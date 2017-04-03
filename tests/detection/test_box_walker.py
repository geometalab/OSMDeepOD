from src.detection.box_walker import BoxWalker


def test_load_tile(small_bbox, default_config):
    walker = BoxWalker(small_bbox, configuration=default_config)
    walker.load_tiles()
    assert walker.tile is not None


def test_load_streets(small_bbox, default_config):
    walker = BoxWalker(small_bbox, configuration=default_config)
    walker.load_streets()
    assert walker.streets is not None


def test_walk_no_compare(zurich_bellevue, configuration_no_compare):
    walker = BoxWalker(zurich_bellevue, configuration=configuration_no_compare)
    walker.load_convnet()
    walker.load_tiles()
    walker.load_streets()
    crosswalk_nodes = walker.walk()
    assert crosswalk_nodes is not None
    assert len(crosswalk_nodes) > 0


def test_walk(zurich_bellevue, default_config):
    walker = BoxWalker(zurich_bellevue, configuration=default_config)
    walker.load_convnet()
    walker.load_tiles()
    walker.load_streets()
    crosswalk_nodes = walker.walk()
    assert crosswalk_nodes is not None
    assert len(crosswalk_nodes) == 0


def test_compare_to_bool_true():
    assert BoxWalker._compare_string_to_bool('true')
    assert BoxWalker._compare_string_to_bool('True')
    assert BoxWalker._compare_string_to_bool('yes')
    assert BoxWalker._compare_string_to_bool('Yes')


def test_compare_to_bool_false():
    assert not BoxWalker._compare_string_to_bool('no')
    assert not BoxWalker._compare_string_to_bool('n')
    assert not BoxWalker._compare_string_to_bool('fooboo')
