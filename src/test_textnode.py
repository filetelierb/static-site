import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from node_manipulation import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

        node3 = TextNode("This is not a text node", TextType.ITALIC, None)
        node4 = TextNode("This is a link node", TextType.LINK, "https://test.com")
        node5 = TextNode("This is not a text node", TextType.TEXT, None)
        node6 = TextNode("This is a link node", TextType.LINK, "https://test.com")

        self.assertNotEqual(node,node3)
        self.assertNotEqual(node,node5)
        self.assertEqual(node4, node6)
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_nodes_delimiter(self):
        nodes = [TextNode("This is a text node. This is another text node.", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is a text node. This is another text node.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)
        nodes2 = [TextNode("This is **a bold node**. This is **a text node.", TextType.TEXT)]
        new_nodes2 = split_nodes_delimiter(nodes2, "**", TextType.BOLD)
        expected_nodes2 = [
            TextNode("This is ", TextType.TEXT),
            TextNode("a bold node", TextType.BOLD),
            TextNode(". This is **a text node.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes2, expected_nodes2)

    def test_extract_markdown_images(self):
        text = "Here is an image ![alt text](https://example.com/image.png) in the text."
        images = extract_markdown_images(text)
        expected_images = [("alt text", "https://example.com/image.png")]
        self.assertEqual(images, expected_images)
    def test_extract_markdown_links(self):
        text = "Here is a link [link text](https://example.com) in the text."
        links = extract_markdown_links(text)
        expected_links = [("link text", "https://example.com")]
        self.assertEqual(links, expected_links)

        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        expected_links = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(links, expected_links)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and another [link2](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected_nodes)
if __name__ == "__main__":
    unittest.main()