import unittest

import htmlnode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_not_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        node2 = TextNode(
            "This is a text node", TextType.BOLD, "https://www.example.com"
        )
        self.assertNotEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_type_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.to_html(), "This is a text node")

    def test_bold_text_to_html(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), "<b>This is a bold text node</b>")

    def test_link_to_html(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(
            html_node.to_html(), '<a href="https://www.example.com">This is a link</a>'
        )

    def test_img_to_html(self):
        node = TextNode("Cool Image", TextType.IMAGE, "www.imgsrc.test")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(
            html_node.to_html(), '<img src="www.imgsrc.test" alt="Cool Image"></img>'
        )

    def test_code_to_html(self):
        node = TextNode('"Background Color: "red"', TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.to_html(), '<code>"Background Color: "red"</code>')


if __name__ == "__main__":
    unittest.main()
