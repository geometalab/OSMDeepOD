import math
from geopy import Point
import urllib
import cv2
import numpy as np
from src.service.globalmaptiles import GlobalMercator
from src.base.Constants import Constants

class TileLoader:
    def __init__(self, bbox):
        self.PRELINK = 'https://t3.ssl.ak.tiles.virtualearth.net/tiles/a'
        self.POSTLINK = '.jpeg?g=4401&n=z'

    def __url_to_image(self, url):
        resp = urllib.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return image

    def __build_url(self, quadtree):
        return self.PRELINK + quadtree + self.POSTLINK

    def __download_image(self, quadtree):
        url = self.__build_url(quadtree)
        return self.__url_to_image(url)

    def __download_tiles(self, bbox):
        mercator = GlobalMercator()
        mx, my = mercator.LatLonToMeters(bbox.top, bbox.left)
        tmaxx, tmaxy = mercator.MetersToTile( mx, my, Constants.ZOOM)
        tminx, tminy = mercator.MetersToTile( mx, my, Constants.ZOOM)
        images = []
        for ty in range(tminy, tmaxy+1):
            for tx in range(tminx, tmaxx+1):
                #tilefilename = "%s/%s/%s" % (Constants.ZOOM, tx, ty)
                quadtree = mercator.QuadTree(tx, ty, Constants.ZOOM)
                images.append(self.__download_image(quadtree))
        return images
