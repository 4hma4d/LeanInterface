from lark import Lark, Transformer, v_args
from lark.reconstruct import Reconstructor
import lark
from ...interpreter.interpret import interpret

latex_grammar = open("modules/lat2lean/latex_grammar.lark").read()
lean_grammar = open("modules/lat2lean/lean_grammar.lark").read()
searchl = ["simp", "aesop", "ring_nf", "exact?", "omega", "rw?","norm_num"]

my_parser = Lark(latex_grammar)
my_parse = my_parser.parse

lean_parser = Lark(lean_grammar, maybe_placeholders=False)
reconstructor = Reconstructor(lean_parser)

def toLean(text):
    mode = ""
    s=""
    for l in text.split("\n"): 
        print(l)
        if l.strip()=="<Lean>":
            mode="Lean"
        elif l.strip()=="<Math>": 
            mode="Math"
        elif l.strip()=="<Auto>": 
            s += " := by "
            s2 = s
            ner = interpret(s2+"done")[1]
            found = False
            for x in searchl:
                s2 += x
                s2 += "\n"
                ner2 = interpret(s2)[1]
                print([ner, ner2])
                if ner2 < ner:
                    s = s2
                    found = True
                    break
                else: s2 = s
            if found == False:
                s+= "sorry\n"

        elif mode=="Lean": s+= l; s+="\n"
        elif mode=="Math": 
            tree=my_parse(l)
            s += reconstructor.reconstruct(tree)
        else: 
            print(l)
            assert False
    print(s)
    return s
            

