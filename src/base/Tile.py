from src.base.Bbox import Bbox
from src.base.Node import Node
class Tile:
    def __init__(self):
        self.image = None
        self.bbox = None

    @classmethod
    def from_tile(cls, pil_image, bbox):
        tile = cls()
        tile.image = pil_image
        tile.bbox = bbox
        return tile

    def get_pixel(self, node):
        image_width = self.bbox.right - self.bbox.left
        image_height = self.bbox.top - self.bbox.bottom

        x = node.longitude - self.bbox.left
        y = node.latitude - self.bbox.bottom

        pixel_x =  int(self.image.size[0] * (x/image_width))
        pixel_y = self.image.size[1] - int(self.image.size[1] * (y/image_height))
        return (pixel_x, pixel_y)

    def getNode(self, pixel):
        x = pixel[0]
        y = pixel[1]
        xCount = self.image.size[0]
        yCount = self.image.size[1]
        yPart = (yCount - y) / float(yCount)
        xPart = x / float(xCount)

        latDiff = float(self.bbox.top) - float(self.bbox.bottom)
        lonDiff = float(self.bbox.right) - float(self.bbox.left)

        lat = float(self.bbox.bottom) + latDiff*yPart
        lon = float(self.bbox.left) + lonDiff*xPart

        return Node(lat,lon)

    def getTile_byNode(self, centreNode, side_length):
        centrePixel = self.get_pixel(centreNode)
        x1 = centrePixel[0] - side_length/2
        x2 = centrePixel[0] + side_length/2
        y1 = centrePixel[1] - side_length/2
        y2 = centrePixel[1] + side_length/2

        img =  self.image.crop((x1, y1, x2, y2))
        assert img.size[0] == 50 and img.size[1] == 50
        leftDown = self.getNode((x1,y1))
        rightUp = self.getNode((x2,y2))
        bbox = Bbox.from_leftdown_rightup(leftDown,rightUp)

        return Tile.from_tile(img,bbox)

    def getCentreNode(self):
        diffLat = self.bbox.node_rightup().latitude - self.bbox.node_leftdown().latitude
        diffLon = self.bbox.node_rightup().longitude - self.bbox.node_leftdown().longitude
        node = Node(self.bbox.node_leftdown().latitude + diffLat/2, self.bbox.node_leftdown().longitude + diffLon/2)
        return node

    def show(self):
        self.image.show()