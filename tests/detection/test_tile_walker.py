from src.detection.box_walker import BoxWalker
from src.detection.tile_walker import TileWalker


def test_get_tiles(small_bbox, default_config):
    box_walker = BoxWalker(small_bbox, configuration=default_config)
    box_walker.load_tiles()
    tile_walker = TileWalker(tile=box_walker.tile)
    tiles = tile_walker.get_tiles()
    assert len(tiles) > 1
