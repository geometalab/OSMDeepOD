from src.visualize import drawer
from src.base.bbox import Bbox
from src.detection.box_walker import BoxWalker


def zurich_bellevue():
    return Bbox.from_lbrt(8.5442953706, 47.36628571, 8.5457748771, 47.3674659016)


def rappi():
    return Bbox.from_lbrt(8.8181022825, 47.2263345016, 8.8188113747, 47.2268572692)


def three_king():
    return Bbox.from_lbrt(8.529906, 47.364329, 8.539329, 47.369052)


def draw_streets(tile, streets):
    for street in streets:
        for i in range(len(street.nodes) - 1):
            start = tile.get_pixel(street.nodes[i])
            end = tile.get_pixel(street.nodes[i + 1])
            drawer.line(tile.image, start, end, 'blue')


def draw_small_boxes(tiles, big_tile):
    for tile in tiles:
        node_left_down = tile.bbox.node_left_down()
        node_right_up = tile.bbox.node_right_up()
        start = big_tile.get_pixel(node_left_down)
        end = big_tile.get_pixel(node_right_up)
        drawer.rectangle(big_tile.image, start, end, "red")


def draw_nodes(nodes, tile):
    for node in nodes:
        position = tile.get_pixel(node)
        drawer.point(tile.image, position, '#66ff33')


walker = BoxWalker(bbox=rappi())

walker.configuration.compare = False
walker.configuration.follow_streets = False

#walker.load_streets()
walker.load_tiles()
walker.load_convnet()

#sample_streets = walker.streets
sample_tile = walker.tile
detected_nodes = walker.walk()

#sample_small_tiles = walker._get_tiles_of_box_with_streets(sample_streets, sample_tile)
sample_small_tiles = walker._get_tiles_of_box(sample_tile)
#sample_tile.image.show()
#draw_streets(sample_tile, sample_streets)
#sample_tile.image.show()
draw_small_boxes(sample_small_tiles, sample_tile)
#sample_tile.image.show()
draw_nodes(detected_nodes, sample_tile)

print('Number of detected nodes: ', len(detected_nodes))

sample_tile.image.show()
