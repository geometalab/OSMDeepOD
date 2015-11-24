from src.detection.deep.Convnet import Convnet
import unittest
import glob
from PIL import Image


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

    def test_to_numpy_array(self):
        net = Convnet.from_verbose(False)
        images = self.load_test_images()
        np_arr = net._to_numpy_array(images)
        should_shape = (len(images), 50, 50, 3)
        self.assertEquals(np_arr.shape, should_shape)

    def test_normalize(self):
        net = Convnet.from_verbose(False)
        images = self.load_test_images()
        np_arr = net._to_numpy_array(images)
        x = net._normalize(np_arr)
        should_shape = (len(images), 3, 50, 50)
        self.assertEquals(x.shape, should_shape, msg="Array should be reshaped")
        self.assertAlmostEqual(np_arr[0][49][49][2], x[0][2][49][49] * 255, delta=0.0001, msg="Value should be normalized with 255")


    def test_load_test_images(self):
        images = self.load_test_images()
        self.assertGreater(len(images), 5)

    def load_test_images(self):
        filenames = glob.glob("test_images/*.png")
        images = []
        for file in filenames:
            img = Image.open(file)
            images.append(img)

        return images