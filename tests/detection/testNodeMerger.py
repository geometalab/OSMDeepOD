from src.detection.NodeMerger import NodeMerger
import unittest
from src.base.Node import Node


class NodeMergerTest(unittest.TestCase):

    def test_getNeighbors(self):

        n1 = Node(7.412756, 46.922925, 1)
        n2 = Node(7.412790, 46.922918, 2)
        n3 = Node(7.412797, 46.922942, 3)
        n4 = Node(8.412797, 46.922942, 4)
        n5 = Node(8.412797, 46.922942, 5)
        nodelist = [n1, n2, n3, n4, n5]
        merger = NodeMerger.from_nodelist(nodelist)
        merger._generate_neardict()
        resultList = merger._get_neighbors(n1)
        self.assertEquals(len(resultList), 3)

        resultList = merger._get_neighbors(n4)
        self.assertEquals(len(resultList), 2)

    def test_reduce(self):
        n1 = Node(7.412756, 46.922925, 1)
        n2 = Node(7.412790, 46.922918, 2)
        n3 = Node(7.412797, 46.922942, 3)
        n4 = Node(8.412797, 46.922942, 4)
        n5 = Node(8.412797, 46.922942, 5)
        nodelist = [n1, n2, n3, n4, n5]

        merger = NodeMerger.from_nodelist(nodelist)
        mergedNodes = merger.reduce()
        self.assertEquals(len(mergedNodes), 2)
