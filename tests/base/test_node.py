from src.base.node import Node


def test_instantiate():
    node = Node(47.0, 8.0, 10)
    assert node.latitude == 47.0
    assert node.longitude == 8.0
    assert node.osm_id == 10


def test_instantiate_string():
    node = Node('47.0', '8.0', 10)
    assert node.latitude == 47.0
    assert node.longitude == 8.0
    assert node.osm_id == 10


def test_add_meter(node1):
    node2 = node1.add_meter(3000, 4000)
    distance = node1.get_distance_in_meter(node2)
    assert 3900 < distance < 4100


def test_copy(node1):
    node2 = node1.copy()
    assert node1.latitude == node2.latitude
    assert node1.longitude == node2.longitude
    assert node1.osm_id == node2.osm_id
    assert node1 == node2


def test_node_equality(node1):
    node = Node('47.0', '8.0', 10)
    assert node == node1


def test_node_not_equal(node1, node2):
    assert node1 != node2
