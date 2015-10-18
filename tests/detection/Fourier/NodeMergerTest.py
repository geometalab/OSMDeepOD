from src.detection.fourier.NodeMerger import NodeMerger
import unittest
from src.base.Node import Node





class NodeMergerTest(unittest.TestCase):

    def test_getNeighbors(self):
        n1 = Node(1, 7.412756, 46.922925)
        n2 = Node(2, 7.412790, 46.922918)
        n3 = Node(3, 7.412797, 46.922942)
        n4 = Node(4, 8.412797, 46.922942)
        n5 = Node(5, 8.412797, 46.922942)
        nodelist = [n1, n2, n3, n4, n5]

        merger = NodeMerger.fromNodeList(nodelist)
        merger.generateNearDict()
        resultList = merger.getNeighbors(n1)
        self.assertEquals(len(resultList), 3)

        resultList = merger.getNeighbors(n4)
        self.assertEquals(len(resultList), 2)

    def test_reduce(self):
        n1 = Node(1, 7.412756, 46.922925)
        n2 = Node(2, 7.412790, 46.922918)
        n3 = Node(3, 7.412797, 46.922942)
        n4 = Node(4, 8.412797, 46.922942)
        n5 = Node(5, 8.412797, 46.922942)
        nodelist = [n1, n2, n3, n4, n5]

        merger = NodeMerger.fromNodeList(nodelist)
        mergedNodes = merger.reduce()
        self.assertEquals(len(mergedNodes), 2)