from src.detection.box_walker import BoxWalker
from src.base.tile_drawer import TileDrawer
from examples.zuerich_bellevue import zuerich_bellevue

'''
This example visualizes the results of the boxwalker
'''

walker = BoxWalker(zuerich_bellevue)
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
