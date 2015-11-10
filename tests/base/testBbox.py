import unittest
from src.base.Bbox import Bbox
from src.base.Node import Node

class TestBbox(unittest.TestCase):

    def test_instantiate_from_bltr(self):
        bottom = 47.0
        left = 8.0
        top = 48.0
        right = 9.0
        bbox = Bbox.from_bltr(bottom, left, top, right)
        self.assertTrue(bbox.bottom == bottom)
        self.assertTrue(bbox.left == left)
        self.assertTrue(bbox.top == top)
        self.assertTrue(bbox.right == right)

    def test_instantiate_from_bltr_string(self):
        bottom = '47.0'
        left = '8.0'
        top = '48.0'
        right = '9.0'
        bbox = Bbox.from_bltr(bottom, left, top, right)
        self.assertTrue(bbox.bottom == bottom)
        self.assertTrue(bbox.left == left)
        self.assertTrue(bbox.top == top)
        self.assertTrue(bbox.right == right)

    def test_in_bbox(self):
        bbox = self.Rappi()
        node = Node(47.22, 8.82)
        self.assertTrue(bbox.in_bbox(node))

    def test_not_in_bbox(self):
        bbox = self.Rappi()
        node = Node(48.0, 8.8)
        self.assertFalse(bbox.in_bbox(node))

    def Rappi(self):
        return Bbox.from_lbrt(8.81372, 47.218788, 8.852430, 47.239654)