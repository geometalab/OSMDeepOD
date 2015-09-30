import unittest
from service.ImageLoader import ImageLoader
import os.path
from geopy import Point
from service.ImageGenerator import ImageGenerator
from service.ImagePlotter import ImagePlotter

class TestImageGenerator(unittest.TestCase):


    def testZebraGenerate(self):
        downLeftPoint = Point('47.226043', '8.818360')
        upRightPoint = Point('47.226926', '8.820032')
        path = os.getcwd() + "/generatorImages/"
        imageGenerator = ImageGenerator(path)

        imageGenerator.generate(downLeftPoint,upRightPoint)

        self.assertTrue(os.listdir(path) != [])