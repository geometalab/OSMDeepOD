import unittest
from src.base.Street import Street
from src.base.Node import Node

class TestStreet(unittest.TestCase):

    def test_instantiate_from_info(self):
        street = Street.from_info('Pythonstreet', 1, 'residential')
        self.assertTrue(street.name == 'Pythonstreet')
        self.assertTrue(street.ident == 1)
        self.assertTrue(street.highway == 'residential')

    def test_instantiate_from_nodes(self):
        node1 = Node('47.0', '8.0', 10)
        node2 = Node('48.0', '9.0', 10)
        street = Street.from_nodes(node1, node2)
        self.assertTrue(street.get_left_node() == node1)
        self.assertTrue(street.get_right_node() == node2)
