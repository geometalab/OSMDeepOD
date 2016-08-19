from src.detection.box_walker import BoxWalker
from src.detection.street_walker import StreetWalker
from src.base.tile_drawer import TileDrawer
from examples.zuerich_bellevue import zuerich_bellevue

'''
Visualizes the 50x50 images which are cutted out of the tile along the streets
Red square are the 50x50 boxes
blue lines are the streets
'''


def load_tile_streets(bbox):
    box_walker = BoxWalker(bbox)
    box_walker.load_tiles()
    box_walker.load_streets()
    return box_walker.tile, box_walker.streets


def cut_squared_images(streets, tile):
    squared_list = []
    for street in streets:
        walker = StreetWalker(tile)
        squared = walker.get_tiles(street)
        squared_list += squared
    return squared_list


def draw(tile, streets, squared_images):
    drawer = TileDrawer.from_tile(tile)

    for street in streets:
        drawer.draw_line(street.nodes[0], street.nodes[1])

    for t in squared_images:
        drawer.draw_box(t.get_centre_node(), 50)

    return drawer


# Loads all tiles and streets within bbox
tile, streets = load_tile_streets(zuerich_bellevue)

squared_list = cut_squared_images(streets, tile)  # Cuts the 50x50 images along the streets

# Draws the streets and marks the squared images on the tile
drawer = draw(tile, streets, squared_list)

drawer.show()
