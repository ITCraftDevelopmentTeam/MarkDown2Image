from . import parser
from . import style
from rich import print

def md2img(markdown: str, output_path: str) -> None:
    ast = style.init_style(style.init_links(parser.parse(markdown)))
    size = style.get_size(ast)
    style.draw(ast, size).save(output_path)
