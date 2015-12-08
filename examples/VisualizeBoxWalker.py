from src.detection.BoxWalker import BoxWalker
from src.base.Bbox import Bbox
from src.base.TileDrawer import TileDrawer

'''
This example visualizes the results of the boxwalker
'''

zurich_bellevue = Bbox.from_bltr(47.224553, 8.816052, 47.227839, 8.820165)
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
