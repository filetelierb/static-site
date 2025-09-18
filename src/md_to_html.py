from block_manipulation import markdown_to_blocks, block_to_block_type, BlockType
from textnode import text_node_to_html_node
from htmlnode import LeafNode, ParentNode
from node_manipulation import text_to_textnodes
import re
def paragraph_block_to_html_node(block):
    text_nodes = text_to_textnodes(block)
    leaf_nodes = []
    for text_node in text_nodes:
        text_node.text = text_node.text.replace("\n", " ")
        leaf_node = text_node_to_html_node(text_node)
        leaf_nodes.append(leaf_node)
    return ParentNode("p", leaf_nodes)

def heading_block_to_html_node(block):
    if block.startswith("# "):
        level = 1
        content = block[2:].strip()
    elif block.startswith("## "):
        level = 2
        content = block[3:].strip()
    elif block.startswith("### "):
        level = 3
        content = block[4:].strip()
    elif block.startswith("#### "):
        level = 4
        content = block[5:].strip()
    elif block.startswith("##### "):
        level = 5
        content = block[6:].strip()
    elif block.startswith("###### "):
        level = 6
        content = block[7:].strip()
    else:
        raise ValueError("Invalid heading block")
    text_nodes = text_to_textnodes(content)
    leaf_nodes = []
    for text_node in text_nodes:
        leaf_node = text_node_to_html_node(text_node)
        leaf_nodes.append(leaf_node)
    return ParentNode(f"h{level}", leaf_nodes)

def code_block_to_html_node(block):
    content = block[3:-3].strip()
    ''' text_nodes = text_to_textnodes(content)
    leaf_nodes = []
    for text_node in text_nodes:
        leaf_node = text_node_to_html_node(text_node)
        leaf_nodes.append(leaf_node)'''
    return ParentNode("pre", [LeafNode("code", content)])

def quote_block_to_html_node(block):
    lines = block.split("\n")
    quote_lines = [line[1:].strip() for line in lines]
    content = "\n".join(quote_lines)
    text_nodes = text_to_textnodes(content)
    leaf_nodes = []
    for text_node in text_nodes:
        leaf_node = text_node_to_html_node(text_node)
        leaf_nodes.append(leaf_node)
    return ParentNode("blockquote", leaf_nodes)

def unordered_list_block_to_html_node(block):
    lines = block.split("\n")
    list_items = [line[2:].strip() for line in lines]
    li_nodes = []
    for item in list_items:
        text_nodes = text_to_textnodes(item)
        leaf_nodes = []
        for text_node in text_nodes:
            leaf_node = text_node_to_html_node(text_node)
            leaf_nodes.append(leaf_node)
        li_node = ParentNode("li", leaf_nodes)
        li_nodes.append(li_node)
    return ParentNode("ul", li_nodes)

def ordered_list_block_to_html_node(block):
    lines = block.split("\n")
    list_items = [re.sub(r"^\d+\.\s", "", line).strip() for line in lines]
    li_nodes = []
    for item in list_items:
        text_nodes = text_to_textnodes(item)
        leaf_nodes = []
        for text_node in text_nodes:
            leaf_node = text_node_to_html_node(text_node)
            leaf_nodes.append(leaf_node)
        li_node = ParentNode("li", leaf_nodes)
        li_nodes.append(li_node)
    return ParentNode("ol", li_nodes)


def extract_title(markdown):
    print(f"Markdown: {markdown}")
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:].strip()
    raise ValueError("No title found in markdown")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                html_node = paragraph_block_to_html_node(block)
                html_nodes.append(html_node)
            case BlockType.HEADING:
                html_node = heading_block_to_html_node(block)
                html_nodes.append(html_node)
            case BlockType.CODE:
                html_node = code_block_to_html_node(block)
                html_nodes.append(html_node)
            case BlockType.QUOTE:
                html_node = quote_block_to_html_node(block)
                html_nodes.append(html_node)
            case BlockType.UNSORTED_LIST:
                html_node = unordered_list_block_to_html_node(block)
                html_nodes.append(html_node)
            case BlockType.OREDERED_LIST:
                html_node = ordered_list_block_to_html_node(block)
                html_nodes.append(html_node)
            case _:
                html_node = paragraph_block_to_html_node(block)
                html_nodes.append(html_node)
            
    
    parent_node = ParentNode("div", html_nodes)
    return parent_node