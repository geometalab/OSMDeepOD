import pytest

from src.data.orthofoto.tile_loader import TileLoader


@pytest.fixture(scope='module')
def image_api():
    return WmsApi()


def test_satellite_image_download(zurich_bellevue, image_api):
    bbox = zurich_bellevue
    tl = TileLoader(bbox, image_api=image_api)
    tile = tl.load_tile()
    img = tile.image
    assert img.size[0] > 0
    assert img.size[1] > 0


def test_new_bbox(small_bbox, image_api):
    tile_loader = TileLoader(small_bbox, image_api)
    tile_loader.load_tile()
    tile = tile_loader.tile
    tile_bbox = tile.bbox
    assert tile_bbox == small_bbox
