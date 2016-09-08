from src.base.node import Node


class Bbox(object):
    def __init__(self):
        self.left = None
        self.bottom = None
        self.right = None
        self.top = None

    @classmethod
    def from_lbrt(cls, left, bottom, right, top):
        bbox = cls()
        bbox.left = left
        bbox.bottom = bottom
        bbox.right = right
        bbox.top = top
        return bbox

    @classmethod
    def from_bltr(cls, bottom, left, top, right):
        bbox = cls()
        bbox.left = left
        bbox.bottom = bottom
        bbox.right = right
        bbox.top = top
        return bbox

    @classmethod
    def from_leftdown_rightup(cls, node_leftdown, node_rightup):
        bbox = cls()
        bbox.left = node_leftdown.longitude
        bbox.bottom = node_leftdown.latitude
        bbox.right = node_rightup.longitude
        bbox.top = node_rightup.latitude
        return bbox

    def node_left_down(self):
        return Node(self.bottom, self.left)

    def node_right_up(self):
        return Node(self.top, self.right)

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
        ret = Bbox.from_leftdown_rightup(new_left_down, new_right_up)
        return ret

    def __str__(self):
        return str(self.bottom) + ',' + str(self.left) + ',' + str(self.top) + ',' + str(self.right)

    def __eq__(self, other):
        return self.bottom == other.bottom and self.left == other.left \
               and self.top == other.top and self.right == other.right
