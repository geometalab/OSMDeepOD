from src.service.TilesLoader.TileLoader import TileLoader
from src.base.Tile import Tile
from src.base.Bbox import Bbox
from PIL import Image


class TileProxy:
    def __init__(self, bbox):
        self.bbox = bbox
        loader = TileLoader()
        self.tiles = loader.download19(self.bbox)

    def getTileByPoint(self, point):
        if(not self.bbox.inBbox(point)): raise Exception("Point not in bbox")

        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[0])):
                tile = self.tiles[y][x]
                if(tile.bbox.inBbox(point)):
                    return tile
        raise Exception("No tile found. Programm error! Call Severin Buehler")

    def getTileIndexes(self, point):
        if(not self.bbox.inBbox(point)): raise Exception("Point not in bbox")
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[0])):
                tile = self.tiles[y][x]
                if(tile.bbox.inBbox(point)):
                    return (y,x)


    def getBigTile(self, node1, node2):
        tileId1 = self.getTileIndexes(node1)
        tileId2 = self.getTileIndexes(node2)
        image = self.mergeImage(tileId1,tileId2)

        return Tile(image, Bbox(node1.longitude, node1.latitude, node2.longitude, node2.latitude))

    def mergeImage(self, tileId1, tileId2):
        yCount = tileId2[0] - tileId1[0] + 1
        xCount = tileId2[1] - tileId1[1] + 1
        width, height = self.tiles[0][0].image.size

        result = Image.new("RGBA", (xCount * width, yCount * height))

        for y in range(yCount):
            for x in range(xCount):
                tiley = tileId1[0] + y
                tilex = tileId1[1] + x

                result.paste(self.tiles[tiley][tilex].image, (x * width, (yCount - y - 1) * height))

        return result

