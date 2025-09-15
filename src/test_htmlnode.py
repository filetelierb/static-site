import unittest

from htmlnode import HTMLNode,LeafNode,ParentNode

class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        html_node1 = HTMLNode("p","Hello world",None,None)
        html_node2 = HTMLNode("a",
                              "Link",
                              None,{
                                    "href": "https://www.google.com",
                                    "target": "_blank",
                                })
        html_node3 = HTMLNode("d","Hello world",html_node1,None)
        
        self.assertEqual(html_node2.props_to_html()," href=\"https://www.google.com\" target=\"_blank\"")
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
if __name__ == "__main__":
    unittest.main()