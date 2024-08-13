from lark import Lark, Transformer, v_args
from lark.reconstruct import Reconstructor
import lark
from .id import id
from .latex import latex 
from .auto import auto

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
            s+= id.toLean(l)
        elif mode=="Math": 
            s += latex.toLean(l)
        else: 
            print(l)
            assert False
    
    final = auto.toLean(s)
    print(final)
    return final
