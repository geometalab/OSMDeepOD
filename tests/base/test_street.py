from src.base.street import Street


def test_instantiate_from_nodes(node1, node2):
    street = Street([node1, node2])
    assert street.nodes[0] == node1
    assert street.nodes[1] == node2
