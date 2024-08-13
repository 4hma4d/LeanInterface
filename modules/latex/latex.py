from lark import Lark, Transformer, v_args
from lark.reconstruct import Reconstructor
import lark

latex_grammar = open("modules/latex/latex_grammar.lark").read()
lean_grammar = open("modules/latex/lean_grammar.lark").read()

my_parser = Lark(latex_grammar)
my_parse = my_parser.parse

lean_parser = Lark(lean_grammar, maybe_placeholders=False)
reconstructor = Reconstructor(lean_parser)

def toLean(l):
    tree=my_parse(l)
    return reconstructor.reconstruct(tree)
