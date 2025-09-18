from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType
from enum import Enum
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        split_texts = node.text.split(delimiter)
        if len(split_texts) <= 2:
            new_nodes.append(node)
            continue
        for i in range(len(split_texts)):
            if i % 2 == 0 and i + 2 < len(split_texts):
                new_nodes.append(TextNode(split_texts[i], TextType.TEXT))
            elif i % 2 == 0 and i + 2 == len(split_texts):
                new_nodes.append(TextNode("**".join([split_texts[i],split_texts[i+1]]), TextType.TEXT))
                break
            elif i + 1 == len(split_texts):
                new_nodes.append(TextNode(split_texts[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_texts[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        text = node.text
        for i in range (len(images)):
            alt, url = images[i]
            parts = text.split(f"![{alt}]({url})", 1)
            new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = parts[1]
        if text and i + 1 == len(images):
            new_nodes.append(TextNode(text, TextType.TEXT))
        
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        text = node.text
        for i in range (len(links)):
            link_text, url = links[i]
            parts = text.split(f"[{link_text}]({url})", 1)
            new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            text = parts[1]
        if text and i + 1 == len(links):
            new_nodes.append(TextNode(text, TextType.TEXT))
        
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes