from src.base.Node import Node

class Bbox:
    def __init__(self, left = 0.0, bottom = 0.0, right = 0.0, top = 0.0):
        self.nodeDownLeft = Node(bottom, left)
        self.nodeUpright = Node(top, right)
        self.left = self.nodeDownLeft.longitude
        self.bottom = self.nodeDownLeft.latitude
        self.right = self.nodeUpright.longitude
        self.top = self.nodeUpright.latitude