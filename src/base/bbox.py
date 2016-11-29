from src.base.node import Node


class Bbox:
    def __init__(self, left=None, bottom=None, right=None, top=None):
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top

    @classmethod
    def from_nodes(cls, node_left_down=None, node_right_up=None):
        bbox = cls()
        bbox.left = node_left_down.longitude
        bbox.bottom = node_left_down.latitude
        bbox.right = node_right_up.longitude
        bbox.top = node_right_up.latitude
        return bbox

    def node_left_down(self):
        return Node(self.bottom, self.left)

    def node_left_up(self):
        return Node(self.top, self.left)

    def node_right_up(self):
        return Node(self.top, self.right)

    def node_right_down(self):
        return Node(self.bottom, self.right)

    def in_bbox(self, node):
        lat = node.latitude
        lon = node.longitude

        in_lat = self.bottom <= lat <= self.top
        in_lon = self.left <= lon <= self.right

        return in_lat and in_lon

    def get_bbox_exclude_border(self, border_distance):
        left_down_node = self.node_left_down()
        right_up_node = self.node_right_up()

        new_left_down = left_down_node.add_meter(border_distance, border_distance)
        new_right_up = right_up_node.add_meter(-border_distance, -border_distance)
        ret = Bbox.from_nodes(node_left_down=new_left_down, node_right_up=new_right_up)
        return ret

    def __str__(self):
        return str(self.bottom) + ',' + str(self.left) + ',' + str(self.top) + ',' + str(self.right)

    def __eq__(self, other):
        return self.bottom == other.bottom and self.left == other.left \
               and self.top == other.top and self.right == other.right
