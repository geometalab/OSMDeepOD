from src.base.Bbox import Bbox
from src.detection.BoxWalker import BoxWalker
from src.detection.StreetWalker import StreetWalker
from src.base.TileDrawer import TileDrawer

'''
Visualizes the 50x50 images which are cutted out of the tile along the streets
Red square are the 50x50 boxes
blue lines are the streets
'''

def load_tile_streets(bbox):
    boxwalker = BoxWalker(bbox, False)
    boxwalker.load_tiles()
    boxwalker.load_streets()
    return boxwalker.tile, boxwalker.streets

def cut_squared_images(streets, tile):
    squared_list = []
    for street in streets:
        walker = StreetWalker.from_street_tile(street, tile, None)
        squared = walker._get_squared_tiles(walker.street.nodes[0], walker.street.nodes[1])
        squared_list += squared
    return squared_list

def draw(tile, streets, squared_images):
    drawer = TileDrawer.from_tile(tile)

    for street in streets:
        drawer.draw_line(street.nodes[0], street.nodes[1])

    for t in squared_images:
        drawer.draw_box(t.getCentreNode(), 50)

    return drawer

zurich_bellevue = Bbox.from_lbrt(8.54279671719532, 47.366177501999516, 8.547088251618977, 47.36781249586627)

(tile, streets) = load_tile_streets(zurich_bellevue) # Loads all tiles and streets within bbox

squared_list = cut_squared_images(streets, tile) # Cuts the 50x50 images along the streets

drawer = draw(tile,streets,squared_list) # Draws the streets and marks the squared images on the tile

drawer.show()


