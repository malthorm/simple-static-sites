import unittest

from textnode import TextType, TextNode
from markdown_handler import split_nodes_delimiter


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
