from src.detection.deep.training.Crosswalk_dataset import Crosswalk_dataset, Categorie, Sample
import unittest
import os


class testCrosswalk_dataset(unittest.TestCase):

    @staticmethod
    def get_test_dataset_path():
        return os.path.dirname(__file__)  + "/dataset/"

    def testDataset_read_samples(self):
        dataset_path = self.get_test_dataset_path()
        instance = Crosswalk_dataset.from_sourcefolder(dataset_path)
        instance.read_samples()
        nb_samples = 10
        self.assertEquals(len(instance.samples_shuffled), nb_samples)
        self.assertGreater(len(instance.samples_crosswalk.samples), 0)
        self.assertGreater(len(instance.samples_nocrosswalk.samples), 0)

    def test_dataset_split(self):
        dataset_path = self.get_test_dataset_path()
        factor = 0.6
        testinstance = Crosswalk_dataset.from_sourcefolder(dataset_path)
        testinstance.read_samples()
        (train_set, test_set) = testinstance.split_train_test(factor)
        self.assertEquals(len(train_set.samples_shuffled), 6)
        self.assertEquals(len(test_set.samples_shuffled), 4)

    def test_dataset_split_nodouble(self):
        dataset_path = self.get_test_dataset_path()
        factor = 0.5
        instance = Crosswalk_dataset.from_sourcefolder(dataset_path)
        instance.read_samples()
        (train_set, test_set) = instance.split_train_test(factor)
        for test_sample in test_set.samples_shuffled:
            for train_sample in train_set.samples_shuffled:
                self.assertNotEqual(test_sample.filepath, train_sample.filepath)

    def test_dataset_load_images(self):
        dataset_path = self.get_test_dataset_path()
        instance = Crosswalk_dataset.from_sourcefolder(dataset_path)
        instance.read_samples()
        instance.load_images()
        self.assertIsNotNone(instance.samples_shuffled[0].pil_image)

    def test_dataset_to_input_response(self):
        dataset_path = self.get_test_dataset_path()
        instance = Crosswalk_dataset.from_sourcefolder(dataset_path)
        instance.read_samples()
        instance.load_images()
        (inputs, responses) = instance.to_input_response()
        should_input_shape = (10, 3, 50, 50)
        should_response_shape = (10,2)
        self.assertEquals(inputs.shape, should_input_shape)
        self.assertEquals(responses.shape, should_response_shape)



    def testCategorie_read_folder(self):
        dataset_path = self.get_test_dataset_path()
        folder = dataset_path + "crosswalks/"
        cat = Categorie.from_default(folder, [1, 0])
        cat.read_folder()
        self.assertEquals(len(cat.samples), 4)

    def testCategorie_tag(self):
        tag = [1, 0]
        dataset_path = self.get_test_dataset_path()
        folder = dataset_path + "crosswalks/"
        cat = Categorie.from_default(folder, tag)
        cat.read_folder()
        self.assertEquals(cat.samples[0].tag, tag)

    def testSample_ctor(self):
        dataset_path = self.get_test_dataset_path()
        filepath = dataset_path + "crosswalks/crosswalk1.png"
        tag = [1, 0]
        sample = Sample.from_file(filepath, tag)
        self.assertEquals(sample.filepath, filepath)
        self.assertEquals(sample.tag, tag)
        self.assertIsNone(sample.pil_image)
        self.assertIsNone(sample.numpy_array)

    def testSample_load(self):
        dataset_path = self.get_test_dataset_path()
        filepath = dataset_path + "crosswalks/crosswalk1.png"
        tag = [1, 0]
        sample = Sample.from_file(filepath, tag)
        sample.load_image()
        self.assertIsNotNone(sample.pil_image)
        self.assertIsNotNone(sample.numpy_array)
