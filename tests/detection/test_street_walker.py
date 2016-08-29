from src.detection.box_walker import BoxWalker
from src.detection.street_walker import StreetWalker


def get_tile_streets(bbox):
    box_walker = BoxWalker(bbox)
    box_walker.load_tiles()
    box_walker.load_streets()
    return box_walker.tile, box_walker.streets


def test_from_street_tile(small_bbox, square_image_length):
    (tile, streets) = get_tile_streets(small_bbox)
    walker = StreetWalker(tile=tile, square_image_length=square_image_length)
    assert walker.tile is not None
    assert streets is not None
