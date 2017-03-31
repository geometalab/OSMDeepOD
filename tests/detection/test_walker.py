from src.detection.box_walker import BoxWalker
from src.detection.walker import Walker


def test_calculate_step_distance():
    walker = Walker()
    step_distance = walker._calculate_step_distance(zoom_level=19)
    assert step_distance > 0


def test_get_squared_tiles(small_bbox, default_config):
    box_walker = BoxWalker(small_bbox, configuration=default_config)
    box_walker.load_tiles()
    walker = Walker(tile=box_walker.tile)
    centre_node = box_walker.tile.get_centre_node()
    tile = walker._get_squared_tiles([centre_node])
    assert len(tile) is 1
