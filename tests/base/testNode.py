import unittest
from src.base.Node import Node


class TestNode(unittest.TestCase):

    def test_instantiate(self):
        node = Node(47.0, 8.0, 10)
        self.assertTrue(node.latitude == 47.0)
        self.assertTrue(node.longitude == 8.0)
        self.assertTrue(node.osm_id == 10)

    def test_instantiate_string(self):
        node = Node('47.0', '8.0', 10)
        self.assertTrue(node.latitude == 47.0)
        self.assertTrue(node.longitude == 8.0)
        self.assertTrue(node.osm_id == 10)

    def test_add_meter(self):
        node1 = Node('47.0', '8.0', 10)
        node2 = node1.add_meter(3000, 4000)
        distance = node1.get_distance_in_meter(node2)
        self.assertTrue(3900 < distance < 4100)

    def test_copy(self):
        node1 = Node('47.0', '8.0', 10)
        node2 = node1.copy()
        self.assertTrue(node1.latitude == node2.latitude)
        self.assertTrue(node1.longitude == node2.longitude)
        self.assertTrue(node1.osm_id == node2.osm_id)
