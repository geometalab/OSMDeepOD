import pytest

from src.base.tile import Tile
from src.base.bbox import Bbox


@pytest.fixture(scope="module")
def tile(small_bbox):
    return Tile(None, small_bbox)


def test_instantiate_from_tile(tile, small_bbox):
    assert tile.bbox.bottom == small_bbox.bottom


def test_tile_get_node(tile, small_bbox):
    node = tile.get_centre_node()
    assert small_bbox.in_bbox(node)


def test_get_centre_node():
    bbox = Bbox(left=0.0, right=2.0, bottom=0.0, top=2.0)
    simple_tile = Tile(image=None, bbox=bbox)
    centre_node = simple_tile.get_centre_node()
    assert centre_node.latitude == 1.0
    assert centre_node.longitude == 1.0
