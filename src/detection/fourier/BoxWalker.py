from src.detection.fourier.StreetWalker import StreetWalker
from src.service.TilesLoader.TileProxy import TileProxy
from src.service.StreetLoader.StreetLoader import StreetLoader
import datetime


class BoxWalker:
    def __init__(self, bbox):
        self.bbox = bbox

    def loadData(self):
        self.out("Loading images within bounding box")
        self.proxy = TileProxy(self.bbox)
        self.out("Images loaded")

        self.out("Loading streets within bounding box")
        streetLoader = StreetLoader()
        self.streets = streetLoader.getStreets(self.bbox)
        self.out("Streets loaded")

    def walk(self):
        self.out("Start walking")
        crosswalkNodes = []
        for street in self.streets:
            streetwalker = StreetWalker(street, self.proxy)
            streetResults =  streetwalker.walk()
            crosswalkNodes += streetResults

        self.out("Finish walking")
        return crosswalkNodes

    def out(self,msg):
        print str(datetime.datetime.now()) + ": " + msg
