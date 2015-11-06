import unittest
from src.role.Manager import Manager
from src.base.Bbox import Bbox
from src.base.Node import Node
from src.base.Constants import Constants

class TestManager(unittest.TestCase):

    def test(self):
        manager = Manager()
        manager.big_bbox = self.big_bbox()
        columns = manager._calc_columns()
        rows = manager._calc_rows()
        self.assertTrue(rows > 40)
        self.assertTrue(columns > 2)

    def test_with_two_columns(self):
        node1 = Node('47.0', '8.0', 10)
        node2 = node1.add_meter(200, Constants.SMALL_BBOX_SIDE_LENGHT + 50)

        manager = Manager()
        bbox = Bbox.from_leftdown_rightup(node1, node2)
        manager.big_bbox = bbox
        columns = manager._calc_columns()
        rows = manager._calc_rows()
        self.assertTrue(rows == 1)
        self.assertTrue(columns == 2)

    def test_with_two(self):
        node1 = Node('47.0', '8.0', 10)
        node2 = node1.add_meter(Constants.SMALL_BBOX_SIDE_LENGHT + 50, Constants.SMALL_BBOX_SIDE_LENGHT + 50)

        manager = Manager()
        bbox = Bbox.from_leftdown_rightup(node1, node2)
        manager.big_bbox = bbox
        columns = manager._calc_columns()
        rows = manager._calc_rows()
        self.assertTrue(rows == 2)
        self.assertTrue(columns == 2)

    def test_with_three(self):
        node1 = Node('47.0', '8.0', 10)
        node2 = node1.add_meter(2 * Constants.SMALL_BBOX_SIDE_LENGHT + 50, 2 * Constants.SMALL_BBOX_SIDE_LENGHT + 50)

        manager = Manager()
        bbox = Bbox.from_leftdown_rightup(node1, node2)
        manager.big_bbox = bbox
        columns = manager._calc_columns()
        rows = manager._calc_rows()
        self.assertTrue(rows == 3)
        self.assertTrue(columns == 3)



    def big_bbox(self):
        return Bbox.from_lbrt(8.8, 47.0, 8.9, 47.9)