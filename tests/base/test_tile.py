import pytest

from src.base.tile import Tile


@pytest.fixture(scope="module")
def tile(small_bbox):
    return Tile(None, small_bbox)


def test_instantiate_from_tile(tile, small_bbox):
    assert tile.bbox.bottom == small_bbox.bottom


def test_tile_get_node(tile, small_bbox):
    node = tile.get_centre_node()
    assert small_bbox.in_bbox(node)
