from src.detection.deep.training.Crosswalk_dataset import Crosswalk_dataset, Categorie, Sample
import unittest


class testCrosswalk_dataset(unittest.TestCase):
    def testDataset_read_samples(self):
        set = Crosswalk_dataset.from_sourcefolder("dataset/")
        set.read_samples()
        nb_samples = 10
        self.assertEquals(len(set.samples_shuffled), nb_samples)
        self.assertGreater(len(set.samples_crosswalk.samples), 0)
        self.assertGreater(len(set.samples_nocrosswalk.samples), 0)

    def test_dataset_split(self):
        factor = 0.6
        set = Crosswalk_dataset.from_sourcefolder("dataset/")
        set.read_samples()
        (train_set, test_set) = set.split_train_test(factor)
        self.assertEquals(len(train_set.samples_shuffled), 6)
        self.assertEquals(len(test_set.samples_shuffled), 4)

    def test_dataset_split_nodouble(self):
        factor = 0.5
        set = Crosswalk_dataset.from_sourcefolder("dataset/")
        set.read_samples()
        (train_set, test_set) = set.split_train_test(factor)
        for test_sample in test_set.samples_shuffled:
            for train_sample in train_set.samples_shuffled:
                self.assertNotEqual(test_sample.filepath, train_sample.filepath)

    def test_dataset_load_images(self):
        set = Crosswalk_dataset.from_sourcefolder("dataset/")
        set.read_samples()
        set.load_images()
        self.assertIsNotNone(set.samples_shuffled[0].pil_image)

    def test_dataset_to_input_response(self):
        set = Crosswalk_dataset.from_sourcefolder("dataset/")
        set.read_samples()
        set.load_images()
        (inputs, responses) = set.to_input_response()
        should_input_shape = (10, 3, 50, 50)
        should_response_shape = (10,2)
        self.assertEquals(inputs.shape, should_input_shape)
        self.assertEquals(responses.shape, should_response_shape)



    def testCategorie_read_folder(self):
        folder = "dataset/crosswalks/"
        cat = Categorie.from_default(folder, [1, 0])
        cat.read_folder()
        self.assertEquals(len(cat.samples), 4)

    def testCategorie_tag(self):
        tag = [1, 0]
        folder = "dataset/crosswalks/"
        cat = Categorie.from_default(folder, tag)
        cat.read_folder()
        self.assertEquals(cat.samples[0].tag, tag)

    def testSample_ctor(self):
        filepath = "dataset/crosswalks/crosswalk1.png"
        tag = [1, 0]
        sample = Sample.from_file(filepath, tag)
        self.assertEquals(sample.filepath, filepath)
        self.assertEquals(sample.tag, tag)
        self.assertIsNone(sample.pil_image)
        self.assertIsNone(sample.numpy_array)

    def testSample_load(self):
        filepath = "dataset/crosswalks/crosswalk1.png"
        tag = [1, 0]
        sample = Sample.from_file(filepath, tag)
        sample.load_image()
        self.assertIsNotNone(sample.pil_image)
        self.assertIsNotNone(sample.numpy_array)
