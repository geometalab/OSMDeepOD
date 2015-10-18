from src.service.TilesLoader.TileProxy import TileProxy
from src.service.StreetLoader.StreetLoader import StreetLoader
from src.service.ImagePlotter import ImagePlotter

class StreetDrawer:
    def __init__(self, bbox):
        self.bbox = bbox

    def downloadTiles(self):
        self.proxy = TileProxy(self.bbox)

    def downloadStreets(self):
        streetloader = StreetLoader()
        self.streets = streetloader.getStreets(self.bbox)


    def drawImage(self):
        box = self.proxy.bbox
        self.tile = self.proxy.getBigTile(box.getDownLeftPoint(), box.getUpRightPoint())
        self.tile.startDrawing()
        for street in self.streets:
            self.tile.drawLine(street.nodes[0].toPoint(), street.nodes[1].toPoint())
        self.tile.stopDrawing()

    def showImage(self):
        plotter = ImagePlotter()
        plotter.plot(self.tile.image)


    def getTiles(self):
        self.downloadData()
        return self.proxy.getTiles()

    def drawImageFromGoogel(self, bigTile):
        streetloader = StreetLoader()
        self.streets = streetloader.getStreets(self.bbox)
        bigTile.startDrawing()
        for street in self.streets:
            bigTile.drawLine(street.nodes[0].toPoint(), street.nodes[1].toPoint())
        bigTile.stopDrawing()
