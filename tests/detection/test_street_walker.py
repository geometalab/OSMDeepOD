from src.base.bbox import Bbox
from src.detection.box_walker import BoxWalker
from src.detection.street_walker import StreetWalker
from src import cwenv


def small_bbox():
    return Bbox.from_lbrt(8.54279671719532, 47.366177501999516, 8.543088251618977, 47.36781249586627)


def get_tile_streets(bbox):
    boxwalker = BoxWalker(
            bbox,
            api_key=cwenv('MAPQUEST_API_KEY'),
            verbose=False)
    boxwalker.load_tiles()
    boxwalker.load_streets()
    return boxwalker.tile, boxwalker.streets


def test_from_street_tile():
    (tile, streets) = get_tile_streets(small_bbox())
    walker = StreetWalker.from_street_tile(streets[0], tile, None)
    assert walker.tile is not None
    assert walker.street is not None
