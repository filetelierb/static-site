from enum import Enum
from htmlnode import LeafNode,ParentNode

class TextType(Enum):
    TEXT = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6

class TextNode:
    def __init__(self, text, text_type, url= None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (self.text == other.text and 
                self.text_type == other.text_type and 
                self.url == other.url)
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    text = text_node.text if text_node.text else ""
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None,text,None)
            
        case TextType.BOLD:
            return LeafNode("b",text,None)

        case TextType.ITALIC:
            return LeafNode("i",text,None)

        case TextType.CODE:
            return LeafNode("code",text,None)

        case TextType.LINK:
            return LeafNode("a",text,{"href": text_node.url})

        case TextType.IMAGE:
            return LeafNode("img","",{"alt":text_node.text,"src":text_node.url})
