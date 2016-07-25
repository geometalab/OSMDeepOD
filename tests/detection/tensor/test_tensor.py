import os
import environ

from src.base.tile_drawer import TileDrawer
from src.detection.box_walker import BoxWalker
from src.base.bbox import Bbox
from src import cwenv


def bern():
    return Bbox.from_lbrt(7.4342250824, 46.9492503237, 7.4393320084, 46.9523726881)


def small_bern():
    return Bbox.from_lbrt(7.4364352226, 46.948893886, 7.4368187785, 46.9494117525)


def caslano():
    return Bbox.from_lbrt(8.878787756, 45.9721151751, 8.8803809881, 45.9744061776)


cwenv = environ.Env(MAPQUEST_API_KEY=(str, 'api_key'))
root = environ.Path(os.getcwd())
environ.Env.read_env(root('.env'))

walker = BoxWalker(caslano(), api_key=cwenv('MAPQUEST_API_KEY'))
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
