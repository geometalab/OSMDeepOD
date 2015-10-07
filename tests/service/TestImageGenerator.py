import unittest
import os.path

from src.service.ImageGenerator import ImageGenerator
from src.base.Bbox import Bbox


class TestImageGenerator(unittest.TestCase):

    '''
    def testZebraGenerate(self):
        bbox = Bbox('8.818360', '47.226043', '8.820032', '47.226926')
        path = os.getcwd() + "/generatorImages/"
        imageGenerator = ImageGenerator(path)

        imageGenerator.generateCrosswalks(bbox)

        self.assertTrue(os.listdir(path) != [])
    '''

    #winti down left 47.486478, 8.703949  up right 47.506433, 8.737978
    def testZebraRapi(self):
        path = "/home/murthy/Projects/SA/positive/winti/"

        bbox = Bbox('8.703949', '47.486478', '8.737978', '47.506433')

        imageGenerator = ImageGenerator(path)

        imageGenerator.generateCrosswalks(bbox)

        self.assertTrue(os.listdir(path) != [])

    '''
    #rapi zebra down left 47.223505, 8.815292 up right 47.235126, 8.847341
    def testZebraRapi(self):
        path = "/home/murthy/Projects/SA/positive/rapi/"

        bbox = Bbox('8.815292', '47.223505', '8.84734', '47.235126')

        imageGenerator = ImageGenerator(path)

        imageGenerator.generateCrosswalks(bbox)

        self.assertTrue(os.listdir(path) != [])

    '''

    #mels down left 47.043556, 9.416240  up right 47.046026, 9.426942
    '''
    def testNoZebraMels(self):
        path = "/home/murthy/Projects/SA/negative/mels/"

        bbox = Bbox('9.416240', '47.043556', '9.426942', '47.046026')

        imageGenerator = ImageGenerator(path)

        imageGenerator.generate(bbox)

        self.assertTrue(os.listdir(path) != [])
    '''

    '''
    #down left 46.187747, 6.128354  up right 46.203332, 6.157744
    def testZebraGeneratorGenf(self):
        path = "/home/murthy/Projects/SA/positive/genf/"

        #Zebra Zuerich
        bbox = Bbox('6.128354', '46.187747', '6.157744', '46.203332')

        imageGenerator = ImageGenerator(path)

        imageGenerator.generateCrosswalks(bbox)

        self.assertTrue(os.listdir(path) != [])
    '''

    '''
    def testZebraGeneratorZuerich(self):
        path = "/home/murthy/Projects/SA/positive/zuerich/"

        #Zebra Zuerich
        bbox = Bbox('8.516459', '47.366062', '8.546671', '47.386928')

        imageGenerator = ImageGenerator(path)

        imageGenerator.generateCrosswalks(bbox)

        self.assertTrue(os.listdir(path) != [])
    '''

    '''
    #Tscherlach No Zebra 47.116819, 9.329320

    def testZebraGeneratorZuerich(self):
        path = "/home/murthy/Projects/SA/haarTraining/negativeImages/"

        #Zebra Zuerich
        downLeftPoint = Point('47.116819', '9.329320')
        upRightPoint = Point('47.119009', '9.340264')

        imageGenerator = ImageGenerator(path)

        imageGenerator.generate(downLeftPoint, upRightPoint)

        self.assertTrue(os.listdir(path) != [])
    '''