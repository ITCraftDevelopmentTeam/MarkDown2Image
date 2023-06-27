from . import parser
from . import style
from rich import print

def md2img(markdown: str, out_path: str):
    ast = style.init_style(parser.parse(markdown))
    print(ast, "\n")
    size = style.get_size(ast)
    print(ast, "\n")
    style.draw(ast, size).show()
