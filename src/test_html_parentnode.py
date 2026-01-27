import unittest

from htmlnode import LeafNode, ParentNode


class TestHTMLLeafNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchild(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node1 = LeafNode("b", "grandchild1")
        grandchild_node2 = LeafNode("b", "grandchild2")
        grandchild_node3 = LeafNode("b", "grandchild3")
        child_node = ParentNode(
            "span", [grandchild_node1, grandchild_node2, grandchild_node3]
        )
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild1</b><b>grandchild2</b><b>grandchild3</b></span></div>",
        )

    def test_to_html_with_multiple_children_and_grandchildren(self):
        grandchild_node1 = LeafNode("b", "grandchild1")
        grandchild_node2 = LeafNode("b", "grandchild2")
        grandchild_node3 = LeafNode("b", "grandchild3")
        grandchild_node4 = LeafNode("b", "grandchild4")
        grandchild_node5 = LeafNode("b", "grandchild5")
        grandchild_node6 = LeafNode("b", "grandchild6")
        child_node1 = ParentNode(
            "span", [grandchild_node1, grandchild_node2, grandchild_node3]
        )
        child_node2 = ParentNode(
            "span", [grandchild_node4, grandchild_node5, grandchild_node6]
        )
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild1</b><b>grandchild2</b><b>grandchild3</b></span><span><b>grandchild4</b><b>grandchild5</b><b>grandchild6</b></span></div>",
        )

    def test_to_html_with_greatgrandchildren_and_prop(self):
        greatgrandchild_node = LeafNode("b", "grandchild")
        grandchild_node = ParentNode(
            "a", [greatgrandchild_node], {"href": "example.com"}
        )
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span><a href="example.com"><b>grandchild</b></a></span></div>',
        )

    def test_to_html_with_raw_text_child(self):
        child_node = LeafNode(None, "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div>child</div>")


if __name__ == "__main__":
    unittest.main()
