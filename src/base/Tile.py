
class Tile:
    def __init__(self):
        self.image = None
        self.bbox = None

    @classmethod
    def from_tile(cls, pilimage, bbox):
        tile = cls()
        tile.image = pilimage
        tile.bbox = bbox
        return tile

    def getPixel(self, node):
        imagewidth = self.bbox.right - self.bbox.left
        imageheight = self.bbox.top - self.bbox.bottom

        x = node.longitude - self.bbox.left
        y = node.latitude - self.bbox.bottom

        pixelX =  int(self.image.size[0] * (x/imagewidth))
        pixelY = self.image.size[1] - int(self.image.size[1] * (y/imageheight))
        return (pixelX, pixelY)

    def show(self):
        self.image.show()