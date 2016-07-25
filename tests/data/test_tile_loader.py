from src.data.tile_loader import TileLoader
from src.base.bbox import Bbox


def zurich_bellevue():
    return Bbox.from_lbrt(8.54279671719532, 47.366177501999516, 8.547088251618977, 47.36781249586627)


def small_bbox():
    return Bbox.from_lbrt(8.54279671719532, 47.366177501999516, 8.543088251618977, 47.36781249586627)


def test_satellite_image_download():
    bbox = zurich_bellevue()
    tl = TileLoader.from_bbox(bbox, False)
    tile = tl.load_tile()
    img = tile.image
    assert img.size[0] == 1792
    assert img.size[1] == 1280


def test_new_bbox():
    tile_loader = TileLoader.from_bbox(small_bbox(), False)
    tile_loader.load_tile()
    tile = tile_loader.tile
    tile_bbox = tile.bbox
    assert abs(tile_bbox.left - 8.5425567627)
    assert abs(tile_bbox.bottom - 47.3658039665) < 0.00001
    assert abs(tile_bbox.right - 8.5432434082) < 0.00001
    assert abs(tile_bbox.top - 47.3681292923) < 0.00001


