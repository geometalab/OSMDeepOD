from src.detection.box_walker import BoxWalker
from src.detection.street_walker import StreetWalker


def get_tile_streets(bbox):
    boxwalker = BoxWalker(
            bbox,
            verbose=False)
    boxwalker.load_tiles()
    boxwalker.load_streets()
    return boxwalker.tile, boxwalker.streets


def test_from_street_tile(small_bbox):
    (tile, streets) = get_tile_streets(small_bbox)
    walker = StreetWalker.from_street_tile(streets[0], tile, None)
    assert walker.tile is not None
    assert walker.street is not None
