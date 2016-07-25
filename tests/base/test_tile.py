from src.base.tile import Tile
from src.base.bbox import Bbox


def rappi():
    return Bbox.from_lbrt(8.81372, 47.218788, 8.852430, 47.239654)


def test_instantiate_from_tile():
    tile = Tile.from_tile(None, rappi())
    assert tile.bbox.bottom == rappi().bottom
