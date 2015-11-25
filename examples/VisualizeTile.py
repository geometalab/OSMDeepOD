from src.data.TileLoader import TileLoader
from src.base.Bbox import Bbox

'''
Download all tiles in a specific BBox
'''

zurich_bellevu = Bbox.from_lbrt(8.54279671719532, 47.366177501999516, 8.547088251618977, 47.36781249586627)
tl = TileLoader.from_bbox(zurich_bellevu)
tile = tl.load_tile()
tile.show()