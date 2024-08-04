from lark import Lark, Transformer, v_args
from lark.reconstruct import Reconstructor
import lark

latex_grammar = open("modules/lat2lean/latex_grammar.lark").read()
lean_grammar = open("modules/lat2lean/lean_grammar.lark").read()


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
        elif mode=="Lean": s+= l; s+="\n"
        elif mode=="Math": 
            tree=my_parse(l)
            s += reconstructor.reconstruct(tree)
        else: 
            print(l)
            assert False
    print(s)
    return s
            

