import pytest

from src.detection.node_merger import NodeMerger
from src.base.node import Node


@pytest.fixture
def node_list():
    n1 = Node(7.412756, 46.922925, 1)
    n2 = Node(7.412790, 46.922918, 2)
    n3 = Node(7.412797, 46.922942, 3)
    n4 = Node(8.412797, 46.922942, 4)
    n5 = Node(8.412797, 46.922942, 5)
    return [n1, n2, n3, n4, n5]


def test_get_neighbors(node_list):
    merger = NodeMerger.from_nodelist(node_list)
    merger._generate_near_dict()
    result_list = merger._get_neighbors(node_list[0])
    assert len(result_list) == 3

    result_list = merger._get_neighbors(node_list[3])
    assert len(result_list) == 2


def test_reduce(node_list):
    merger = NodeMerger.from_nodelist(node_list)
    merged_nodes = merger.reduce()
    assert len(merged_nodes) == 2


def test_reduce_same_points():
    node1 = Node(46.78351333884473, 8.159137666225423, 10)
    node2 = Node(46.78351333884473, 8.159137666225423, 10)
    merger = NodeMerger.from_nodelist([node1,node2])
    merged_nodes = merger.reduce()
    assert len(merged_nodes) == 1



