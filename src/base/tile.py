from src.base.bbox import Bbox
from src.base.node import Node


class Tile:
    def __init__(self, image, bbox):
        self.image = image
        self.bbox = bbox

    def get_pixel(self, node):
        image_width = self.bbox.right - self.bbox.left
        image_height = self.bbox.top - self.bbox.bottom

        x = node.longitude - self.bbox.left
        y = node.latitude - self.bbox.bottom

        pixel_x = int(self.image.size[0] * (x / image_width))
        pixel_y = self.image.size[1] - int(self.image.size[1] * (y / image_height))
        return pixel_x, pixel_y

    def get_node(self, pixel):
        x = pixel[0]
        y = pixel[1]
        x_count = self.image.size[0]
        y_count = self.image.size[1]
        y_part = (y_count - y) / float(y_count)
        x_part = x / float(x_count)

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

        img = self.image.crop((x1, y1, x2, y2))
        left_down = self.get_node((x1, y1))
        right_up = self.get_node((x2, y2))
        bbox = Bbox.from_leftdown_rightup(left_down, right_up)

        return Tile(img, bbox)

    def get_centre_node(self):
        diff_lat = self.bbox.node_right_up().latitude - self.bbox.node_left_down().latitude
        diff_lon = self.bbox.node_right_up().longitude - self.bbox.node_left_down().longitude
        node = Node(self.bbox.node_left_down().latitude + diff_lat / 2,
                    self.bbox.node_left_down().longitude + diff_lon / 2)
        return node

    def show(self):
        self.image.show()
