import unittest
from src.role.Manager import Manager
from src.base.Bbox import Bbox
from src.base.Node import Node


class TestManager(unittest.TestCase):

    def test(self):
        manager = Manager(bbox=self.big_bbox(), jobqueue_name='dummy')
        columns = manager._calc_columns()
        rows = manager._calc_rows()
        self.assertTrue(rows > 40)
        self.assertTrue(columns > 2)

    def test_with_two_columns(self):
        node1 = Node('47.0', '8.0', 10)
        node2 = node1.add_meter(200, Manager.SMALL_BBOX_SIDE_LENGHT + 50)
        manager = Manager(
            bbox=Bbox.from_leftdown_rightup(
                node1,
                node2),
            jobqueue_name='dummy')
        columns = manager._calc_columns()
        rows = manager._calc_rows()
        self.assertTrue(rows == 1)
        self.assertTrue(columns == 2)

    def test_first(self):
        node1 = Node('47.0', '8.0', 10)
        node2 = Node('47.1', '8.1', 10)
        manager = Manager(
            bbox=Bbox.from_leftdown_rightup(
                node1,
                node2),
            jobqueue_name='dummy')
        manager._generate_small_bboxes()
        self.assertTrue(manager.small_bboxes[0].left == node1.longitude)
        self.assertTrue(manager.small_bboxes[0].bottom == node1.latitude)

    def test_big_bbox(self):
        node1 = Node('47.0', '8.0', 10)
        node2 = Node('47.5', '8.5', 10)
        manager = Manager(
            bbox=Bbox.from_leftdown_rightup(
                node1,
                node2),
            jobqueue_name='dummy')
        length = len(manager.small_bboxes)
        manager._generate_small_bboxes()
        self.assertTrue(manager.small_bboxes[0].left == node1.longitude)
        self.assertTrue(manager.small_bboxes[0].bottom == node1.latitude)
        self.assertTrue(
            manager.small_bboxes[
                length -
                1].right >= node2.longitude and manager.small_bboxes[
                length -
                1].right <= node2.longitude +
            0.05)
        self.assertTrue(
            manager.small_bboxes[
                length -
                1].top >= node2.latitude and manager.small_bboxes[
                length -
                1].top <= node2.latitude +
            0.05)

    def test_with_two(self):
        node1 = Node('47.0', '8.0', 10)
        node2 = node1.add_meter(
            Manager.SMALL_BBOX_SIDE_LENGHT +
            50,
            Manager.SMALL_BBOX_SIDE_LENGHT +
            50)
        manager = Manager(
            bbox=Bbox.from_leftdown_rightup(
                node1,
                node2),
            jobqueue_name='dummy')
        columns = manager._calc_columns()
        rows = manager._calc_rows()
        self.assertTrue(rows == 2)
        self.assertTrue(columns == 2)

    def test_with_three(self):
        node1 = Node('47.0', '8.0', 10)
        node2 = node1.add_meter(
            2 *
            Manager.SMALL_BBOX_SIDE_LENGHT +
            50,
            2 *
            Manager.SMALL_BBOX_SIDE_LENGHT +
            50)
        manager = Manager(
            bbox=Bbox.from_leftdown_rightup(
                node1,
                node2),
            jobqueue_name='dummy')
        columns = manager._calc_columns()
        rows = manager._calc_rows()
        self.assertTrue(rows == 3)
        self.assertTrue(columns == 3)

    @staticmethod
    def big_bbox():
        return Bbox.from_lbrt(8.8, 47.0, 8.9, 47.9)
