from src.base.street import Street


def test_instantiate_from_info():
    street = Street.from_info('Pythonstreet', 1, 'residential')
    assert street.name == 'Pythonstreet'
    assert street.ident == 1
    assert street.highway == 'residential'


def test_instantiate_from_nodes(node1, node2):
    street = Street.from_nodes(node1, node2)
    assert street.get_left_node() == node1
    assert street.get_right_node() == node2
