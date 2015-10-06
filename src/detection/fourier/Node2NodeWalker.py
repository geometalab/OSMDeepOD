from src.service.ImagePlotter import ImagePlotter

class Node2NodeWalker:
    def __init__(self, node1, node2, images):
        self.node1 = node1
        self.node2 = node2
        self.images = images

    def walk(self):
        print "walk"
