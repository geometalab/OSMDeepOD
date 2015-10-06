import httplib2
from StringIO import StringIO
from PIL import Image
from src.base.Tile import Tile


class TileLoader:
    # http://dev.virtualearth.net/REST/V1/Imagery/Map/Aerial/
    # ?mapArea=47.366177501999516,8.54279671719532,47.36781249586627,8.547088251618977
    # &key=Asc0mfX_vbDVHkleWyc85z1mRLrSfjqHeGJamZsRF-mgzR4_GAlU31hkwMOGN4Mq

    def __init__(self):
        self.PRELINK = "ttp://dev.virtualearth.net/REST/V1/Imagery/Map/Aerial/?mapArea="
        self.POSTLINK = "&key=Asc0mfX_vbDVHkleWyc85z1mRLrSfjqHeGJamZsRF-mgzR4_GAlU31hkwMOGN4Mq"

    def download(self, bbox):
        url = self.PRELINK + bbox.toString() + self.POSTLINK
        resp, content = httplib2.Http().request(url)
        image = Image.open(StringIO(content))
        return Tile(image,bbox)

    def downloadZoom19(self):
