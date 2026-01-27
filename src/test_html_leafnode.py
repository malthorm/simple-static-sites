import unittest

from htmlnode import LeafNode


class TestHTMLLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p_with_props(self):
        node = LeafNode("p", "Hello, world!", {"attr": "value", "foo": "bar"})
        self.assertEqual(node.to_html(), '<p attr="value" foo="bar">Hello, world!</p>')

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "follow me", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">follow me</a>')

    def test_leaf_without_tag(self):
        node = LeafNode(None, "This is just raw text")
        self.assertEqual(node.to_html(), "This is just raw text")


if __name__ == "__main__":
    unittest.main()
