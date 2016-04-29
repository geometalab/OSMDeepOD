from src.detection.deep.Convnet import Convnet
import unittest
import glob
from PIL import Image
import os


class testConvnet(unittest.TestCase):
    def testInitialize_model_is_loaded(self):
        net = Convnet.from_verbose(False)
        net.initialize()
        self.assertTrue(net.is_initialized())
        self.assertIsNotNone(net.model)

    def test_predict(self):
        images = self.load_test_images()
        net = Convnet.from_verbose(False)
        net.initialize()
        result = net.predict_crosswalks(images)
        self.assertEquals(len(images), len(result), msg="Number of images is unequal number of results")

    def test_threshold(self):
        images = self.load_test_images()
        net = Convnet.from_verbose(False)
        net.initialize()
        net.threshold = -1
        results = net.predict_crosswalks(images)

        for res in results:
            self.assertEquals(res, True)


    def test_load_test_images(self):
        images = self.load_test_images()
        self.assertGreater(len(images), 5)

    def load_test_images(self):
        filenames = glob.glob(self.get_dataset_path() + "*.png")
        images = []
        for image_file in filenames:
            img = Image.open(image_file)
            images.append(img)

        return images

    @staticmethod
    def get_dataset_path():
        return os.path.dirname(__file__) + "/test_images/"