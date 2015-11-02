from src.base.Node import Node

class Bbox:

    def __init__(self):
        self.left = None
        self.bottom = None
        self.right = None
        self.top = None

    @classmethod
    def from_lbrt(cls, left, bottom, right, top):
        box = cls()
        box.left = left
        box.bottom = bottom
        box.right = right
        box.top = top
        return box

    @classmethod
    def from_bltr(cls, bottom, left, top, right):
        box = cls()
        box.left = left
        box.bottom = bottom
        box.right = right
        box.top = top
        return box

    @classmethod
    def from_bltr(cls, node_leftdown, node_rightup):
        box = cls()
        box.left = node_leftdown.longitude
        box.bottom = node_leftdown.latitude
        box.right = node_rightup.longitude
        box.top = node_rightup.latitude
        return box

    def __str__(self):
        return "Bbox left: " + str(self.left) + " bottom: " + str(self.bottom) + " right: " + str(self.right) + " top: " + self.top

    def node_leftdown(self):
        return Node(self.bottom, self.left)

    def node_rightup(self):
        return Node(self.top, self.right)

    def in_bbox(self, node):
        lat = node.latitude
        lon = node.longitude

        inLat = lat >= float(self.bottom) and lat <= float(self.top)
        intLon = lon >= float(self.left) and lon <= float(self.right)

        return inLat and intLon

    def centerpoint(self):
        lon = self.left + ((self.right - self.left) / 2)
        lat = self.bottom + ((self.top - self.bottom) / 2)
        return Node(lat, lon)
