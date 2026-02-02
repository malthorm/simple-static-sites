import unittest

from textnode import TextType, TextNode
from markdown_handler import (
    BlockType,
    block_to_block_type,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    markdown_to_html_node,
    extract_title,
)


class TestMarkdownHanlder(unittest.TestCase):
    def test_plain_text(self):
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.TEXT)
        expected_nodes = [
            TextNode("This is just plain text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_do_not_split_non_text_type_nodes(self):
        node = TextNode("this is bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [TextNode("this is bold", TextType.BOLD)]
        self.assertEqual(new_nodes, expected_nodes)

    def test_text_with_inline_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_text_with_inline_start(self):
        node = TextNode("**This** is text with a bold start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This", TextType.BOLD),
            TextNode(" is text with a bold start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_text_with_inline_end(self):
        node = TextNode("This is text with a italic _end_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("This is text with a italic ", TextType.TEXT),
            TextNode("end", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_text_with_inline_chain(self):
        node = TextNode("This is text with _a_ _italic_ _end_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("a", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("end", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_no_additional_text(self):
        matches = extract_markdown_images("![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_dont_extract_markdown_images_with_bad_format(self):
        matches = extract_markdown_images("[image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a paragraph with a [link](https://www.example.com)."
        )
        self.assertListEqual([("link", "https://www.example.com")], matches)

    def test_extract_two_markdown_links(self):
        matches = extract_markdown_links(
            "This is a paragraph with a [link](https://www.example.com), and then [another](www.test.de)."
        )
        self.assertListEqual(
            [("link", "https://www.example.com"), ("another", "www.test.de")], matches
        )

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

    def test_split_images_without_img(self):
        node = TextNode("There is no image link here", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("There is no image link here", TextType.TEXT)], new_nodes
        )

    def test_split_images_from_multiple_nodes(self):
        node1 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        node3 = TextNode("There is no image link here", TextType.TEXT)
        new_nodes = split_nodes_image([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("There is no image link here", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_with_only_images(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![image](https://i.imgur.com/zjjcJKZ.png)![image](https://i.imgur.com/zjjcJKZ.png)![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and nothing more",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" and nothing more", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_two_links_with_text_between(self):
        node = TextNode(
            "This is the [first](www.first.com) and now comes [another](https://someaddr.com) with text at the end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is the ", TextType.TEXT),
                TextNode("first", TextType.LINK, "www.first.com"),
                TextNode(" and now comes ", TextType.TEXT),
                TextNode("another", TextType.LINK, "https://someaddr.com"),
                TextNode(" with text at the end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_multiple_nodes_with_two_links_with_text_between(self):
        node1 = TextNode(
            "This is the [first](www.first.com) and now comes [another](https://someaddr.com) with text at the end",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is the [first](www.first.com) and now comes [another](https://someaddr.com) with text at the end",
            TextType.TEXT,
        )
        node3 = TextNode("and one with just text", TextType.TEXT)
        new_nodes = split_nodes_link([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode("This is the ", TextType.TEXT),
                TextNode("first", TextType.LINK, "www.first.com"),
                TextNode(" and now comes ", TextType.TEXT),
                TextNode("another", TextType.LINK, "https://someaddr.com"),
                TextNode(" with text at the end", TextType.TEXT),
                TextNode("This is the ", TextType.TEXT),
                TextNode("first", TextType.LINK, "www.first.com"),
                TextNode(" and now comes ", TextType.TEXT),
                TextNode("another", TextType.LINK, "https://someaddr.com"),
                TextNode(" with text at the end", TextType.TEXT),
                TextNode("and one with just text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_with_no_links_in_text(self):
        node = TextNode("Just some text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("Just some text", TextType.TEXT)], new_nodes)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_with_plain_text(self):
        text = "This is just some text"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("This is just some text", TextType.TEXT)],
            new_nodes,
        )

    def test_text_to_textnodes_with_chained_markup(self):
        text = "**bold**_italic_`code`![img](www.src.com)plain"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode("code", TextType.CODE),
                TextNode("img", TextType.IMAGE, "www.src.com"),
                TextNode("plain", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_to_text_with_invalid_markdown(self):
        text = "**bold**_italic_`code`![img](www.src.com)plain"
        new_nodes = text_to_textnodes(text)
        self.assertRaises(ValueError)

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

    def test_markdown_to_blocks_with_excessive_newlines(self):
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

    def test_markdown_to_blocks_with_trailing_whitespaces(self):
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

    def test_block_to_blocktype_paragraph(self):
        md = "This is a **bolded** paragraph"
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_block_to_blocktype_heading(self):
        md = "# This is a heading"
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.HEADING, block_type)

    def test_block_to_blocktype_heading_with_malformed_heading(self):
        md = "#This is not a heading"
        block_type = block_to_block_type(md)
        self.assertNotEqual(BlockType.HEADING, block_type)

    def test_block_to_blocktype_heading_with_subheading(self):
        md = "#### This is a sub-heading"
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.HEADING, block_type)

    def test_block_to_blocktype_heading_with_subheading_too_deep(self):
        md = "####### This is not a sub-heading, too many #s"
        block_type = block_to_block_type(md)
        self.assertNotEqual(BlockType.HEADING, block_type)

    def test_block_to_blocktype_code(self):
        md = "```\nThis is a codeblock```"
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.CODE, block_type)

    def test_block_to_blocktype_malformed_codeblock(self):
        md = "```This is not a codeblock```"
        block_type = block_to_block_type(md)
        self.assertNotEqual(BlockType.CODE, block_type)

    def test_block_to_blocktype_block_quote(self):
        md = "> This is a quote\n>and it continues here"
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.QUOTE, block_type)

    def test_block_to_blocktype_malforemd_block_quote(self):
        md = "> This is a quote\nand it continues here> here\n> and here"
        block_type = block_to_block_type(md)
        self.assertNotEqual(BlockType.QUOTE, block_type)

    def test_block_to_blocktype_unordered_list(self):
        md = "- first\n- second\n- third"
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)

    def test_block_to_blocktype_malformed_unordered_list(self):
        md = "- first\n- second\n - third"
        block_type = block_to_block_type(md)
        self.assertNotEqual(BlockType.UNORDERED_LIST, block_type)

    def test_block_to_blocktype_ordered_list(self):
        md = "1. first\n2. second\n3. third"
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.ORDERED_LIST, block_type)

    def test_block_to_blocktype_malformed_ordered_list_bad_num(self):
        md = "1. first\n2. second\n3x. third"
        block_type = block_to_block_type(md)
        self.assertNotEqual(BlockType.ORDERED_LIST, block_type)

    def test_block_to_blocktype_malformed_ordered_list_bad_ordering(self):
        md = "1. first\n2. second\n4 . third"
        block_type = block_to_block_type(md)
        self.assertNotEqual(BlockType.ORDERED_LIST, block_type)

    def test_block_to_blocktype_malformed_ordered_list_bad_indent(self):
        md = "1. first\n2. second\n3.third"
        block_type = block_to_block_type(md)
        self.assertNotEqual(BlockType.ORDERED_LIST, block_type)

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
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_markdown_headings_to_html(self):
        md = """
# Title

## Intro

Here is some paragraph

###### This just be an h6

####### This has too many #s, so it's a paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Title</h1><h2>Intro</h2><p>Here is some paragraph</p><h6>This just be an h6</h6><p>####### This has too many #s, so it's a paragraph</p></div>",
        )

    def test_markdown__to_html_with_links_and_images(self):
        md = r"""
# Title

## Intro

Here is some paragraph

###### This just be an h6

![Background](some_img.jpg)

[google](https://www.google.com)
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><h1>Title</h1><h2>Intro</h2><p>Here is some paragraph</p><h6>This just be an h6</h6><p><img src="some_img.jpg" alt="Background"></img></p><p><a href="https://www.google.com">google</a></p></div>',
        )

    def test_markdown__to_html_with_ordered_list(self):
        md = r"""
# Ordered List

1. first
2. second
3. third
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Ordered List</h1><ol><li>first</li><li>second</li><li>third</li></ol></div>",
        )

    def test_markdown__to_html_with_unordered_list(self):
        md = r"""
# Ordered List

- first
- second
- third
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Ordered List</h1><ul><li>first</li><li>second</li><li>third</li></ul></div>",
        )

    def test_extract_title_md_only_contains_valid_title(self):
        md = "# This is a title"
        title = extract_title(md)
        self.assertEqual(title, "This is a title")

    def test_extract_title_md_only_contains_invalid_title(self):
        md = "#This is not a title"
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_extract_title_md_empty(self):
        md = ""
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_extract_title_md_with_more_md_content(self):
        md = r"""# Lists

## Unordered list

- first
- second
- third

## Ordered list

1. first
2. second
3. third
"""
        title = extract_title(md)
        self.assertEqual(title, "Lists")

    def test_extract_title_md_with_empty_lines_at_beginning(self):
        md = r"""

# Lists

## Unordered list

- first
- second
- third

## Ordered list

1. first
2. second
3. third
"""
        title = extract_title(md)
        self.assertEqual(title, "Lists")
