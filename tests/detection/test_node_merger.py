import pytest

from src.base.node import Node
from src.data.osm.node_merger import NodeMerger


@pytest.fixture(scope="module")
def node_list():
    n1 = Node(7.41275611, 46.922925, 1)
    n2 = Node(7.41275612, 46.922925, 2)
    n3 = Node(7.41275613, 46.922925, 3)
    n4 = Node(8.412797, 46.922942, 4)
    n5 = Node(8.412797, 46.922941, 5)
    return [n1, n2, n3, n4, n5]


@pytest.fixture(scope="module")
def same_node():
    return Node(46.78351333884473, 8.159137666225423, 10)


@pytest.fixture(scope="module")
def big_node_list():
    return [Node(47.09572760391754, 9.354246854782108, 0.0), Node(47.09569108531167, 9.353826284408573, 0.0),
            Node(47.095734907638715, 9.353978633880619, 0.0), Node(47.091450260764105, 9.347023665904997, 0.0),
            Node(47.09598323415865, 9.353849887847904, 0.0), Node(47.09582072636252, 9.354110956192018, 0.0),
            Node(47.095880982062205, 9.353635311126713, 0.0), Node(47.09582255229281, 9.353581666946415, 0.0)]


def test_get_neighbors(node_list):
    merger = NodeMerger(node_list)
    merger._generate_near_dict()
    result_list = merger._get_neighbors(node_list[0])
    assert len(result_list) == 3

    result_list = merger._get_neighbors(node_list[3])
    assert len(result_list) == 2


def test_reduce(node_list):
    merger = NodeMerger(node_list)
    merged_nodes = merger.reduce()
    assert len(merged_nodes) == 2


def test_reduce_same_points(same_node):
    merger = NodeMerger([same_node, same_node])
    merged_nodes = merger.reduce()
    assert len(merged_nodes) == 1


def test_reduce_not_same_points(same_node):
    node = Node(46.78351333884473, 8.159137666225423, 0)
    merger = NodeMerger([node, same_node])
    merged_nodes = merger.reduce()
    assert len(merged_nodes) == 1


def test_node_merger(big_node_list):
    merger = NodeMerger(big_node_list, 30)
    nodes = merger.reduce()
    assert len(nodes) == 2
