import datetime
from src.detection.fourier.Node2NodeWalker import Node2NodeWalker


class StreetWalker:
    def __init__(self, street, proxy):
        self.street = street
        self.proxy = proxy

    def walk(self):
        self.out(self.street.name)
        node1 = self.street.nodes[0]
        node2 = self.street.nodes[1]
        tile = self.proxy.getBigTileByNodes(node1, node2)


    def out(self,msg):
        print "-" + str(datetime.datetime.now()) + ": " + msg