from textnode import TextNode, TextType

def main():
    text_node_obj = TextNode("Hello, World!", TextType.LINK, "https://www.boot.dev")
    print(text_node_obj)

main()