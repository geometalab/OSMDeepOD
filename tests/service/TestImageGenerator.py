import unittest
import os.path

from src.service.ImageGenerator import ImageGenerator
from src.base.Bbox import Bbox


class TestImageGenerator(unittest.TestCase):

    def testZebraBasel(self):
        #path = "/home/murthy/Projects/SA/images/positive/basel_small/"
        #path = "/home/murthy/Projects/SA/images/positive/zuerich_small/"
        path = "/home/murthy/Projects/SA/images/positive/genf_small/"

        #bbox = Bbox('7.559269', '47.551828', '7.612397', '47.571766') #basel
        #bbox = Bbox('8.516459', '47.366062', '8.546671', '47.386928')
        bbox = Bbox('6.128354', '46.187747', '6.157744', '46.203332')

        imageGenerator = ImageGenerator(path)

        imageGenerator.generateCrosswalks(bbox)

        self.assertTrue(os.listdir(path) != [])
