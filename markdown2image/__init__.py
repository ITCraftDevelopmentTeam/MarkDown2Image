from . import parser
from . import style
from rich import print

def md2img(markdown: str, out_path: str):
    ast = style.init_style(style.init_links(parser.parse(markdown)))
    size = style.get_size(ast)
    print(ast)
    style.draw(ast, size).show()
