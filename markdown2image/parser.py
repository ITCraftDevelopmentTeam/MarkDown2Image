import xml.dom.minidom
import marko

preserve_nodes_for_line_breaks = ["code"]

def markdown2html(markdown: str) -> str:
    print(marko.convert(markdown))
    return f"<div>{marko.convert(markdown)}</div>".replace("\n\n", "<br />")

def parse_dom(nodes: list, parent_node: str | None = None) -> list:
    ast, item = [], {}
    if parent_node == "ol":
        length = 0
    for node in nodes:
        item["type"] = node.nodeName
        item["parentNode"] = parent_node
        if node.attributes != None:
            for attr in node.attributes.items():
                item[attr[0]] = attr[1]
        item["innerHTML"] = parse_dom(node.childNodes, item["type"])
        if item["type"] == "li" and parent_node == "ol":
            length += 1
            item["length"] = length

        if node.nodeType == node.TEXT_NODE:
            if parent_node not in preserve_nodes_for_line_breaks:
                item = node.data.replace("\n", "")
            else:
                item = node.data
        if item:
            ast.append(item)
        item = {}
    return ast

def parse_html(html: str) -> list:
    dom = xml.dom.minidom.parseString(html)
    ast = parse_dom(dom.childNodes)
    print(ast, "\n")
    return ast

def parse(markdown: str) -> list:
    return parse_html(markdown2html(markdown))

     
