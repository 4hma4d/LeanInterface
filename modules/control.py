from lark import Lark, Transformer, v_args
from lark.reconstruct import Reconstructor
import lark
from ..interpreter.interpret import interpret

latex_grammar = open("modules/search/latex_grammar.lark").read()
lean_grammar = open("modules/search/lean_grammar.lark").read()
searchl = ["ring", "aesop"]

my_parser = Lark(latex_grammar)
my_parse = my_parser.parse

lean_parser = Lark(lean_grammar, maybe_placeholders=False)
reconstructor = Reconstructor(lean_parser)

def toLean(text):
    mode = ""
    s=""
    for l in text.split("\n"): 
        if l.strip()=="<Lean>":
            mode="Lean"
        elif l.strip()=="</Lean>": 
            mode=""        
        elif l.strip()=="<Math>": 
            mode="Math"
        elif l.strip()=="</Math>": 
            mode="Lean"
        elif l.strip()=="<Auto>": 
            s += " := by sorry--<Auto> \n"
        elif l.strip()=="<Calc>": 
            s += " := by calc  \n"
        elif l.strip()=="":
            s += "\n"        
        elif mode=="Lean": 
            s+= l; s+= "\n"
            s = s.replace(r"\R", "ℝ")
            s = s.replace(r"\Z", "ℤ")
            s = s.replace(r"\N", "ℕ")
        elif mode=="Math": 
            tree=my_parse(l)
            s += reconstructor.reconstruct(tree)
        else: 
            print(l)
            assert False
    
    final = auto(s)
    print(final)
    return final


def ner(l1, l2):
    return interpret(("".join([x + y for x, y in zip(l1[:-1], l2)]))+l1[-1])[1]

def auto(text):
    l1 = list(text.split("sorry--<Auto>"))
    print(l1)
    working=["sorry"]*(len(l1)-1)
    found = False
    n=-1
    for l in l1[:-1]:
        n+=1
        l2 = ["sorry"]*(len(l1)-1)
        l2[n]="done"
        nerstart = ner(l1,l2)
        for tac in searchl:
            l2[n]=tac
            nerend= ner(l1,l2)
            if nerstart > nerend:
                working[n]=tac
                print(tac)
                break
            else: continue


    return "".join([x + y for x, y in zip(l1[:-1], working)])+l1[-1]
