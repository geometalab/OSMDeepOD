import unittest
import os.path
from geopy import Point
from src.service.ImageGenerator import ImageGenerator
from src.service.Mapquest import Box

class TestImageGenerator(unittest.TestCase):


    def testZebraGenerate(self):
        bbox = Box('8.818360', '47.226043', '8.820032', '47.226926')
        path = os.getcwd() + "/generatorImages/"
        imageGenerator = ImageGenerator(path)

        imageGenerator.generateCrosswalks(bbox)

        self.assertTrue(os.listdir(path) != [])

    def testZebraGeneratorZuerich(self):
        path = "/home/murthy/Projects/SA/haarTraining/positiveImages/"

        #Zebra Zuerich
        bbox = Box('8.516459', '47.366062', '8.546671', '47.386928')

        imageGenerator = ImageGenerator(path)

        imageGenerator.generateCrosswalks(bbox)

        self.assertTrue(os.listdir(path) != [])


    ##Tscherlach No Zebra 47.116819, 9.329320
    '''
    def testZebraGeneratorZuerich(self):
        path = "/home/murthy/Projects/SA/haarTraining/negativeImages/"

        #Zebra Zuerich
        downLeftPoint = Point('47.116819', '9.329320')
        upRightPoint = Point('47.119009', '9.340264')

        imageGenerator = ImageGenerator(path)

        imageGenerator.generate(downLeftPoint, upRightPoint)

        self.assertTrue(os.listdir(path) != [])
    '''