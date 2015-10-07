from src.service.TilesLoader.TileProxy import TileProxy
from src.service.StreetLoader.StreetLoader import StreetLoader
from src.service.ImagePlotter import ImagePlotter

class StreetDrawer:
    def __init__(self, bbox):
        self.bbox = bbox

    def downloadData(self):
        self.proxy = TileProxy(self.bbox)
        streetloader = StreetLoader()
        self.streets = streetloader.getStreets(self.bbox)

    def drawImage(self):
        box = self.proxy.bbox
        self.tile = self.proxy.getBigTile(box.getDownLeftPoint(), box.getUpRightPoint())
        for street in self.streets:
            self.tile.drawLine(street.nodes[0].toPoint(), street.nodes[1].toPoint())

    def showImage(self):
        plotter = ImagePlotter()
        plotter.plot(self.tile.image)


