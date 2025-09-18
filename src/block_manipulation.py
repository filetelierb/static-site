import re

class BlockType:
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNSORTED_LIST = 5
    OREDERED_LIST = 6

def markdown_to_blocks(markdown):
    split_text = markdown.split("\n\n")
    blocks = []
    for text in split_text:
        updated_text = text.strip()
        if updated_text:
            lines = updated_text.split("\n")
            updated_lines = []
            for line in lines:
                updated_lines.append(line.strip())
            updated_text = "\n".join(updated_lines)

            blocks.append(updated_text)
    return blocks

def block_to_block_type(block):
    if block.startswith("# ") or block.startswith("## ") or block.startswith("### ") or block.startswith("#### ") or block.startswith("##### ") or block.startswith("###### "):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        lines = block.split("\n")
        all_match = True
        for line in lines:
            if not line.startswith(">"):
                all_match = False
                break
        if not all_match:
            return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith("- "):
        lines = block.split("\n")
        all_match = True
        for line in lines:
            if not line.startswith("- "):
                all_match = False
                break
        if not all_match:  
            return BlockType.PARAGRAPH
        return BlockType.UNSORTED_LIST
    elif re.match(r"^\d+\.\s", block):
        lines = block.split("\n")
        all_match = True
        for line in lines:
            if not re.match(r"^\d+\.\s", line):
                all_match = False
                break
        if not all_match:  
            return BlockType.PARAGRAPH
        return BlockType.OREDERED_LIST
    else:
        return BlockType.PARAGRAPH
