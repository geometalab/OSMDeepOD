from src.base.Node import Node

class Bbox:

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

    def __str__(self):
        return "Bbox left: " + str(self.left) + " bottom: " + str(self.bottom) + " right: " + str(self.right) + " top: " + str(self.top)

    def node_leftdown(self):
        return Node(self.bottom, self.left)

    def node_rightup(self):
        return Node(self.top, self.right)

    def in_bbox(self, node):
        lat = node.latitude
        lon = node.longitude

        inLat = self.bottom <= lat <= self.top
        inLon = self.left <= lon <= self.right

        return inLat and inLon

    def getBboxExludeBorder(self, borderDistance):
        leftDownNode = self.node_leftdown()
        rightUpNode = self.node_rightup()

        newLeftDown = leftDownNode.add_meter(borderDistance, borderDistance)
        newRightUp = rightUpNode.add_meter(-borderDistance,-borderDistance)
        ret = Bbox.from_leftdown_rightup(newLeftDown,newRightUp)
        return ret
