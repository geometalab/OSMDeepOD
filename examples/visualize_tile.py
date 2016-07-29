from src.data.tile_loader import TileLoader
from src.base.bbox import Bbox

'''
Download all tiles in a specific BBox
'''

zurich_bellevu = Bbox.from_lbrt(
    8.54279671719532,
    47.366177501999516,
    8.547088251618977,
    47.36781249586627)
tl = TileLoader.from_bbox(zurich_bellevu)
tl.load_tile()
tile = tl.tile
tile.show()
