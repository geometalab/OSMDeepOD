from src.detection.fourier.mlp.NeuralNetwork import NeuralNetwork
import unittest
from src.detection.fourier.mlp.DataGenerator import DataGenerator



class TestNeuralNetwork(unittest.TestCase):
    def test_train(self):
        samples = self.generateSamples()
        net = NeuralNetwork()
        net.setDataset(samples)
        net.initialize()
        net.train()

    def generateSamples(self):
        generator = DataGenerator("/home/osboxes/Documents/squaredImages/no/")
        datasN = generator.generateSampleDatabyFolder()

        generator = DataGenerator("/home/osboxes/Documents/squaredImages/yes/")
        datasY = generator.generateSamplesByPixel()
        return datasN[0:len(datasY)] + datasY