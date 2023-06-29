import json
from PIL import ImageFont, Image, ImageDraw
import os.path

path: str = os.path.dirname(os.path.abspath(__file__))
default_style: dict = json.load(open(
    os.path.join(path, "default_style/style.json"), encoding="utf-8"))
nodes_needed_nl: list = ["h1", "h2", "h3", "h4", "h5", "h6", "p"]

def parse_style(item: dict | str | None) -> dict:
    if not item:
        return {}
    elif isinstance(item, str):
        return {}       # TODO 解析 CSS
    else:
        return item

def init_links(_ast: list) -> list:
    ast = _ast.copy()
    for i in range(len(ast)):
        item = ast[i]
        if isinstance(item, dict):
            if item["type"] == "a":
                item["style"] = {"color": "#0000ff"}
                item["innerHTML"].append({
                    "type":      "span",
                    "style":     {"color": "#00ff00"},
                    "innerHTML": [" (", item["href"], ")"]
                })
            else:
                item["innerHTML"] = init_links(item["innerHTML"])
    return ast

def init_style(_ast: list, inherited_style: dict = {}) -> list:
    ast = _ast.copy()
    nlpos = []
    for i in range(len(ast)):
        item = ast[i]
        if isinstance(item, dict):
            _style = (default_style.get(item["type"]) or {}).copy()
            _style.update(inherited_style.copy())
            _style.update(parse_style(item.get("style")).copy())
            item["style"] = _style.copy()
            # print(_style)
            item["innerHTML"] = init_style(item["innerHTML"], item["style"]) 
            nlpos.append(i)
        elif isinstance(item, str):
            _style = (default_style.get("text") or {}).copy()
            _style.update(inherited_style.copy())
            # print(_style)
            ast[i] = {
                "type": "text",
                "style": _style.copy(),
                "innerHTML": [item]
            }
    temp1 = 0
    for pos in nlpos:
        ast.insert(pos + temp1 + 1, {"type": "br", "style": {}, "innerHTML": {}})
        temp1 += 1
    return ast

# TODO 计算自适应

def get_size(ast: list) -> tuple[int, int]:#, list]:
    size = [0, 0]
    line_size = [0, 0]
    for item in ast:
        match item["type"]:
            case "text":
                widget_size = ImageFont.truetype(
                        item["style"].get("font-family") or os.path.join(
                            path, "font/sarasa-fixed-cl-regular.ttf"),
                        item["style"].get("font-size") or\
                                default_style["text"].get("font-size") or 20)\
                        .getsize(item["innerHTML"][0])
            case "br":
                size[0] = max(size[0], line_size[0])
                size[1] += line_size[1]
                line_size = [0, 0]
                continue
            case _:
                widget_size = get_size(item["innerHTML"])
        item["size"] = widget_size
        line_size[0] += widget_size[0]
        line_size[1] += widget_size[1]
    size[0] = max(size[0], line_size[0])
    size[1] += line_size[1]
    return tuple(size)

        
def draw(ast: dict, size: tuple) -> Image:
    img = Image.new("RGB", size, (255, 255, 255)) # TODO
    dr = ImageDraw.Draw(img)
    pos = [0, 0]
    line_height = 0
    for item in ast:
        match item["type"]:
            case "text":
                font = ImageFont.truetype(item["style"].get(
                    "font-family") or os.path.join(
                        path, "font/sarasa-fixed-cl-regular.ttf"
                    ), item["style"].get(
                        "font-size"
                    ) or default_style["text"].get(
                        "font-size"
                    ) or 20
                )
                dr.text(tuple(pos), item["innerHTML"][0],
                        font=font, fill=item["style"].get(
                            "color") or "#000")
                pos[0] += item["size"][0]
                line_height = max(line_height, item["size"][1])
            case "br":
                pos = [0, pos[1] + line_height]
                line_height = 0
            case _:
                img.paste(draw(item["innerHTML"], item["size"]), tuple(pos))
                pos[0] += item["size"][0]
                line_height = max(line_height, item["size"][1])

    return img




    


