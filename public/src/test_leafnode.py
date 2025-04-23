import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):  

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    # def test_with_tag_no_props(self):
    #     node = LeafNode("p", "Hello, world!", {})
    #     self.assertEqual(node.to_html(),'<p>Hello, world!</p>')

    # def test_with_no_tag(self):
    #     node = LeafNode(None, "Just text", {})
    #     self.assertEqual(
    #         node.to_html(),
    #         'Just text'
    #     )

    # def test_missing_value(self):
    #     with self.assertRaises(ValueError):
    #         LeafNode("p", None, {})  # Should raise ValueError