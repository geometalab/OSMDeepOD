from src.base.bbox import Bbox
from src.base.node import Node


class Tile:
    def __init__(self, image_api=None, image=None, bbox=None):
        self.image_api = image_api
        self.image = image
        self.bbox = bbox

    def get_pixel(self, node):
        image_width = self.bbox.right - self.bbox.left
        image_height = self.bbox.top - self.bbox.bottom

        x = node.longitude - self.bbox.left
        y = node.latitude - self.bbox.bottom

        image_size = self.image_api.get_image_size(self.bbox)
        pixel_x = int(image_size[0] * (x / image_width))
        pixel_y = image_size[1] - int(image_size[1] * (y / image_height))
        return pixel_x, pixel_y

    def get_node(self, pixel=(0, 0)):
        x = pixel[0]
        y = pixel[1]
        image_size_x, image_size_y = self.image_api.get_image_size(self.bbox)
        y_part = 0
        x_part = 0
        if image_size_x > 0 and image_size_y > 0:
            y_part = (image_size_y - y) / float(image_size_y)
            x_part = x / float(image_size_x)

        lat_diff = float(self.bbox.top) - float(self.bbox.bottom)
        lon_diff = float(self.bbox.right) - float(self.bbox.left)

        lat = float(self.bbox.bottom) + lat_diff * y_part
        lon = float(self.bbox.left) + lon_diff * x_part

        return Node(lat, lon)

    def get_tile_by_node(self, centre_node, side_length):
        centre_pixel = self.get_pixel(centre_node)
        x1 = centre_pixel[0] - side_length // 2
        x2 = centre_pixel[0] + side_length // 2
        y1 = centre_pixel[1] - side_length // 2
        y2 = centre_pixel[1] + side_length // 2

        crop_box = (x1, y1, x2, y2)
        left_down = self.get_node((x1, y1))
        right_up = self.get_node((x2, y2))
        bbox = Bbox.from_nodes(node_left_down=left_down, node_right_up=right_up)
        img = self.image_api.get_image(bbox)

        return Tile(image=img, bbox=bbox)

    def get_centre_node(self):
        diff_lat = self.bbox.node_right_up().latitude - self.bbox.node_left_down().latitude
        diff_lon = self.bbox.node_right_up().longitude - self.bbox.node_left_down().longitude
        return Node(self.bbox.node_left_down().latitude + diff_lat / 2,
                    self.bbox.node_left_down().longitude + diff_lon / 2)
