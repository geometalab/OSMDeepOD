from src.detection.node_merger import NodeMerger
from src.base.node import Node


def test_get_neighbors():
    n1 = Node(7.412756, 46.922925, 1)
    n2 = Node(7.412790, 46.922918, 2)
    n3 = Node(7.412797, 46.922942, 3)
    n4 = Node(8.412797, 46.922942, 4)
    n5 = Node(8.412797, 46.922942, 5)
    node_list = [n1, n2, n3, n4, n5]
    merger = NodeMerger.from_nodelist(node_list)
    merger._generate_near_dict()
    result_list = merger._get_neighbors(n1)
    assert len(result_list) == 3

    result_list = merger._get_neighbors(n4)
    assert len(result_list) == 2


def test_reduce():
    n1 = Node(7.412756, 46.922925, 1)
    n2 = Node(7.412790, 46.922918, 2)
    n3 = Node(7.412797, 46.922942, 3)
    n4 = Node(8.412797, 46.922942, 4)
    n5 = Node(8.412797, 46.922942, 5)
    nodelist = [n1, n2, n3, n4, n5]

    merger = NodeMerger.from_nodelist(nodelist)
    merged_nodes = merger.reduce()
    assert len(merged_nodes) == 2
