from block_manipulation import markdown_to_blocks, block_to_block_type, BlockType
from md_to_html import markdown_to_html_node, extract_title
import unittest

class TestBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# Heading 1"), 2)
        self.assertEqual(block_to_block_type("## Heading 2"), 2)
        self.assertEqual(block_to_block_type("### Heading 3"), 2)
        self.assertEqual(block_to_block_type("#### Heading 4"), 2)
        self.assertEqual(block_to_block_type("##### Heading 5"), 2)
        self.assertEqual(block_to_block_type("###### Heading 6"), 2)
        self.assertEqual(
            block_to_block_type("```python\nprint('Hello, world!')\n```"), 3
        )
        self.assertEqual(block_to_block_type("> This is a quote"), 4)
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), 5)
        self.assertEqual(block_to_block_type("1. First item\n2. Second item"), 6)
        self.assertEqual(
            block_to_block_type("This is a regular paragraph with text."), 1
        )

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
      
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )
    
    def test_extract_title(self):
        md = """
        # Title of the Document

        This is some content in the document.


        ## Subtitle


        # This is more content.
        """
        title = extract_title(md)
        self.assertEqual(title, "Title of the Document")
if __name__ == "__main__":
    unittest.main()