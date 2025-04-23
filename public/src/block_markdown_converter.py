from enum import Enum
from htmlnode import ParentNode
from inline_markdown_converter import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    # Headings start with 1-6 # characters, followed by a space and then the heading text.
    if block.startswith('#'):
        # Check if it's a valid heading format
        parts = block.split(' ', 1)
        if len(parts) > 1 and 1 <= len(parts[0]) <= 6 and all(char == '#' for char in parts[0]):
            return BlockType.HEADING

    # Code blocks start and end with 3 backticks
    if block.startswith('```') and block.endswith('```'):
        return BlockType.CODE

    # Quote blocks: every line starts with >
    lines = block.split('\n')
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE

    # Unordered lists: every line starts with - followed by a space
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered lists: check for numbered list format
    is_ordered_list = True
    for i, line in enumerate(lines):
        expected_prefix = f"{i+1}. "
        if not line.startswith(expected_prefix):
            is_ordered_list = False
            break
    if is_ordered_list and lines:  # Check that there's at least one line
        return BlockType.ORDERED_LIST

    # If no other conditions match, it's a paragraph
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    # Split by one or more blank lines (two or more newlines)
    blocks = markdown.split('\n\n')

    # Process each block
    result = []
    for block in blocks:
        # Strip leading/trailing whitespace
        cleaned_block = block.strip()

        # Only add non-empty blocks
        if cleaned_block:
            result.append(cleaned_block)
    return result


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    # Convert text to TextNode objects
    text_nodes = text_to_textnodes(text)

    # Convert each TextNode to an HTMLNode
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)

    return html_nodes


def paragraph_to_html_node(block):
    # Replace newlines with spaces to make a single line of text
    block = block.replace("\n", " ")

    # Process inline markdown in block and get children nodes
    children = text_to_children(block)

    # Create paragraph node with children
    paragraph_node = ParentNode("p", children)

    return paragraph_node


def heading_to_html_node(block):
    # Count the heading level (number of # at start)
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break

    # Make sure the heading format is valid
    if level == 0 or level > 6:
        raise ValueError(f"Invalid heading level: {level}")

    # Extract the heading text (skip the # characters and the space after)
    text = block[level:].strip()

    # If there's no text after the # characters, raise an error
    if not text:
        raise ValueError(f"Heading has no text: {block}")

    # Process inline markdown in the heading text
    children = text_to_children(text)

    # Create and return heading node
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    # Verify that the code block has the correct format (starts and ends with ```)
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block: missing ``` delimiters")

    # Extract the content between the ``` markers
    # Start at index 4 (after the opening ``` + newline)
    # End at index -3 (before the closing ```)
    text = block[4:-3]

    # Create a raw text node - we don't parse markdown inside code blocks
    # This ensures special characters like * or _ aren't interpreted as formatting
    raw_text_node = TextNode(text, TextType.TEXT)

    # Convert the text node to an HTML node
    child = text_node_to_html_node(raw_text_node)

    # Create a <code> element containing the code content
    code = ParentNode("code", [child])

    # Wrap the <code> element in a <pre> element for proper HTML formatting
    # <pre> preserves whitespace and line breaks in the output
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    # Split the block into individual list items by newline
    items = block.split("\n")

    # Create an array to hold our list item nodes
    html_items = []

    # Process each list item
    for item in items:
        # Remove the ordered list marker (e.g., "1. ") and any leading whitespace
        # The format is assumed to be "1. Text" or similar with numbers
        text = item[3:]  # Skip the digit, period, and space

        # Process inline markdown in the list item text
        children = text_to_children(text)

        # Create a list item node and add it to our array
        html_items.append(ParentNode("li", children))

    # Create and return an ordered list node containing all the list items
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    # Split the block into individual list items by newline
    items = block.split("\n")

    # Create an array to hold our list item nodes
    html_items = []

    # Process each list item
    for item in items:
        # Remove the unordered list marker (e.g., "- " or "* ") and any leading whitespace
        text = item[2:]  # Skip the marker and space

        # Process inline markdown in the list item text
        children = text_to_children(text)

        # Create a list item node and add it to our array
        html_items.append(ParentNode("li", children))

    # Create and return an unordered list node containing all the list items
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    # Split the block into individual quote lines
    lines = block.split("\n")

    # Create an array to hold the processed lines without the quote markers
    new_lines = []

    # Process each line of the quote
    for line in lines:
        # Verify each line starts with the quote marker ">"
        if not line.startswith(">"):
            raise ValueError(
                "Invalid quote block: all lines must start with '>'")

        # Remove the quote marker and any leading/trailing whitespace
        # lstrip(">") removes all ">" characters from the beginning
        # strip() removes leading/trailing whitespace
        new_lines.append(line.lstrip(">").strip())

    # Join all the lines with spaces to form the quote content
    # This converts multi-line quotes into a single paragraph
    content = " ".join(new_lines)

    # Process inline markdown in the quote content
    children = text_to_children(content)

    # Create and return a blockquote node containing the processed content
    return ParentNode("blockquote", children)
