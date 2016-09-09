from src.visualize import drawer
from src.base.bbox import Bbox
from src.detection.box_walker import BoxWalker


def zurich_bellevue():
    return Bbox.from_lbrt(8.5442953706, 47.36628571, 8.5457748771, 47.3674659016)


def draw_streets(tile, streets):
    for street in streets:
        start = tile.get_pixel(street.nodes[0])
        end = tile.get_pixel(street.nodes[1])
        drawer.line(tile.image, start, end, 'blue')


def draw_small_boxes(tiles, big_tile):
    for tile in tiles:
        node_left_down = tile.bbox.node_left_down()
        node_right_up = tile.bbox.node_right_up()
        start = big_tile.get_pixel(node_left_down)
        end = big_tile.get_pixel(node_right_up)
        drawer.rectangle(big_tile.image, start, end, "red")


walker = BoxWalker(bbox=zurich_bellevue())
walker.load_streets()
walker.load_tiles()
sample_streets = walker.streets
sample_tile = walker.tile
sample_small_tiles = walker._get_tiles_of_box(sample_streets, sample_tile)

draw_streets(sample_tile, sample_streets)
draw_small_boxes(sample_small_tiles, sample_tile)

sample_tile.image.show()
