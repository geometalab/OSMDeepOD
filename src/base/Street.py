from geopy import Point
from geopy.distance import vincenty
import numpy as np

class Street:
    def __init__(self):
        self.nodes = []
        self.name = ""
        self.ident = 0
        self.highway = "-"

    @classmethod
    def from_nodes(cls, node1, node2):
        street = cls()
        street.nodes.append(node1)
        street.nodes.append(node2)

    def getLeftNode(self):
        if(self.nodes[0].logitude < self.nodes[1].longitude):
            return self.nodes[0]
        else:
            return self.nodes[1]

    def getRightNode(self):
        if(self.nodes[0].logitude > self.nodes[1].logitude):
            return self.nodes[0]
        else:
            return self.nodes[1]