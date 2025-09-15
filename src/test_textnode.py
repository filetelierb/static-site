import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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

if __name__ == "__main__":
    unittest.main()