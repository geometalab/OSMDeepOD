from src.detection.box_walker import BoxWalker
from src.base.bbox import Bbox
from src.base.tile_drawer import TileDrawer

'''
This example visualizes the results of the boxwalker
'''

zurich_bellevue = Bbox.from_lbrt(
    8.54279671719532,
    47.366177501999516,
    8.547088251618977,
    47.36781249586627)  # Take the BBox you want

walker = BoxWalker(zurich_bellevue)
walker.load_convnet()
walker.load_tiles()
walker.load_streets()

walker.walk()  # Walk through the streets. This could take some time...

crosswalkNodes = walker.plain_result  # Takes all results found
# crosswalkNodes = walker.compared_with_osm_result # Takes only the
# results which are not already in OSM

# Draw and show the result
drawer = TileDrawer.from_tile(walker.tile)
for node in crosswalkNodes:
    drawer.draw_point(node)
drawer.drawsection.save("boxsave.jpg")
drawer.drawsection.show()
