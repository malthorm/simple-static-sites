import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_empty_node_eq(self):
        node1 = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node1, node2)

    def test__node_eq(self):
        node1 = HTMLNode("a", "This is an anchor", None, {"href": "_"})
        node2 = HTMLNode("a", "This is an anchor", None, {"href": "_"})
        self.assertEqual(node1, node2)

    def test__node_not_eq(self):
        node1 = HTMLNode("a", "This is an anchor", None, {"href": "_"})
        node2 = HTMLNode(
            "a", "This is an anchor", None, {"href": "https://different.de"}
        )
        self.assertNotEqual(node1, node2)

    def test__node_repr(self):
        node1 = HTMLNode("a", "This is an anchor", None, {"href": "_"})
        str_rep = node1.__repr__()
        self.assertEqual(str_rep, "HTMLNode(a, This is an anchor, None, {'href': '_'})")

    def test_empty_props(self):
        node1 = HTMLNode()
        self.assertEqual(node1.props_to_html(), "")

    def test_node_with_props(self):
        node1 = HTMLNode(
            "a",
            "This is an anchor",
            None,
            {"href": "https://example.com", "_target": "_"},
        )
        self.assertEqual(
            node1.props_to_html(), ' href="https://example.com" _target="_"'
        )


if __name__ == "__main__":
    unittest.main()
