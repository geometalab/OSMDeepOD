import unittest
from service.StreetLoader.StreetLoader import StreetLoader
import os.path
from geopy import Point
import cv2
from service.ImagePlotter import ImagePlotter

class TestImageLoader(unittest.TestCase):
    def testLoader(self):
        loader = StreetLoader()
        loader.getStreets("8.815191135900864", "47.22491209728128", "8.823774204748178", "47.22819078179419")