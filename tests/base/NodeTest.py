from src.base.Bbox19 import Bbox19
import unittest
from src.base.Node import Node
from geopy import Point
import numpy as np


class NodeTest(unittest.TestCase):
    def test_StepTo(self):
        node1 = Node.create(Point(47.367362, 8.544548))
        node2 = Node.create(Point(47.367530, 8.544998))
        newNode = node1.stepTo(node2, 10)

        self.assertLess(np.square(newNode.lat - 47.3673932329), 0.0001)
        self.assertLess(np.square(newNode.lon - 8.54467235259), 0.0001)

