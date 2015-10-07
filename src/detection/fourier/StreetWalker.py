import datetime
from src.detection.fourier.Node2NodeWalker import Node2NodeWalker


class StreetWalker:
    def __init__(self, street, proxy):
        self.street = street
        self.proxy = proxy

    def walk(self):
        self.out(self.street.name)
        for idx in range(len(self.street.nodes)-1):
            node1 = self.street.nodes[idx]
            node2 = self.street.nodes[idx + 1]
            nodeWalker = Node2NodeWalker(node1, node2, self.proxy)
            nodeWalker.walk()

    def out(self,msg):
        print "-" + str(datetime.datetime.now()) + ": " + msg