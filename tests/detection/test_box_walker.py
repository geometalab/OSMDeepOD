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

