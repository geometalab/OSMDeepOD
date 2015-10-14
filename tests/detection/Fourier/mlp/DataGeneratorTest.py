from src.detection.fourier.BoxWalker import BoxWalker
import unittest
from src.detection.fourier.mlp.DataGenerator import DataGenerator



class TestDataGenerator(unittest.TestCase):
    def test_generateBySourcefolder(self):
        generator = DataGenerator("/home/osboxes/Documents/squaredImages/no/")
        datas = generator.generateSampleDatabyFolder()
        print datas

    def test_generateBySourceFolderANdBoud(self):
        generator = DataGenerator("/home/osboxes/Documents/squaredImages/yes/")
        datas = generator.generateSamplesByPixel()
        print datas
