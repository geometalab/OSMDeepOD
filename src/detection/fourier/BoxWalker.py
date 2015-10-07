from src.service.ImagePlotter import ImagePlotter
from src.service.TilesLoader.TileProxy import TileProxy
from src.service.StreetLoader.StreetLoader import StreetLoader


class BoxWalker:
    def __init__(self):
        self.streetLoader = StreetLoader()
        self.proxy = TileProxy()

    def walk(self, box):
        streets = self.streetLoader.getStreets(box)
        images = self.imageLoader.downloadImagesByPositions(box.getDownLeftPoint(), box.getUpRightPoint())
        ImagePlotter().plotMatrix(images)
