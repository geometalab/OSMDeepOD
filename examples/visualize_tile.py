from src.data.tile_loader import TileLoader
from examples.zuerich_bellevue import zuerich_bellevue

'''
Download all tiles in a specific BBox
'''

tl = TileLoader(zuerich_bellevue)
tl.load_tile()
tile = tl.tile
tile.show()
