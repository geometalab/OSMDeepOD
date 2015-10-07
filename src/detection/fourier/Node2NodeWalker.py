import datetime
from matplotlib import pyplot as plt


class Node2NodeWalker:
    def __init__(self, node1, node2, proxy):
        self.node1 = node1
        self.node2 = node2

        self.proxy = proxy

    def walk(self):
        self.out(str(self.node1.ident) + " to " + str(self.node2.ident))
        tile = self.proxy.getBigTileByNodes(self.node1, self.node2)
        self.plotTile(tile)

    def out(self,msg):
        print "---" + str(datetime.datetime.now()) + ": " + msg

    def plotTile(self,tile):
        plt.imshow(tile.image)
        plt.show()
