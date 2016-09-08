from src.visualize import drawer
from src.base.bbox import Bbox
from src.data.orthofoto.tile_loader import TileLoader
from src.data.orthofoto.other.other_api import OtherApi


def zurich_bellevue():
    return Bbox.from_lbrt(8.5448316112, 47.3661604928, 8.5453673825, 47.366466604)


def run():
    bbox = zurich_bellevue()
    tl = TileLoader(bbox)
    tile = tl.load_tile()
    node_left_down_bbox = bbox.node_left_down()
    node_right_up_bbox = bbox.node_right_up()

    node_left_down_fitting_box = tile.bbox.node_left_down()
    node_right_up_fitting_box = tile.bbox.node_right_up()
    img = tile.image
    start_bbox = tile.get_pixel(node_left_down_bbox)
    end_bbox = tile.get_pixel(node_right_up_bbox)

    end_fitting_box = tile.get_pixel(node_right_up_fitting_box)
    start_fitting_box = tile.get_pixel(node_left_down_fitting_box)

    drawer.rectangle(img, start_bbox, end_bbox, "red")
    drawer.rectangle(img, start_fitting_box, end_fitting_box, "blue")
    img.show()


def other_api_example():
    bbox = zurich_bellevue()
    other_api = OtherApi()
    image = other_api.get_image(bbox)
    tile = other_api.tile
    node_left_down_bbox = bbox.node_left_down()
    node_right_up_bbox = bbox.node_right_up()
    start_bbox = tile.get_pixel(node_left_down_bbox)
    end_bbox = tile.get_pixel(node_right_up_bbox)

    drawer.rectangle(tile.image, start_bbox, end_bbox, "red")
    tile.image.show()
    image.show()


other_api_example()
