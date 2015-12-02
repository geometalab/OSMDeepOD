from src.detection.BoxWalker import BoxWalker
from src.base.Bbox import Bbox
from src.base.TileDrawer import TileDrawer

'''
This example visualizes the results of the boxwalker
'''

zurich_bellevue = Bbox.from_lbrt(8.814650, 47.222553, 8.825035, 47.228935)
walker = BoxWalker(zurich_bellevue)
walker.load_convnet()
walker.load_tiles()
walker.load_streets()

walker.walk()
crosswalkNodes = walker.plain_result

drawer = TileDrawer.from_tile(walker.tile)
for node in crosswalkNodes:
    drawer.draw_point(node)
drawer.drawsection.save("boxsave.jpg")
drawer.drawsection.show()
