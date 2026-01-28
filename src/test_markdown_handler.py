import unittest

from textnode import TextType, TextNode
from markdown_handler import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
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
