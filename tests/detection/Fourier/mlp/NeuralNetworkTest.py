from src.detection.fourier.mlp.NeuralNetwork import NeuralNetwork
import unittest
from src.detection.fourier.mlp.DataGenerator import DataGenerator
from random import shuffle


class TestNeuralNetwork(unittest.TestCase):


    def test_train(self):
        self.readData()

        net = NeuralNetwork()
        net.setDataset(self.trainSet)
        net.setTestSet(self.testSet)

        net.initialize()


        lasterror = net.train()
        i = 0
        while(True):
            i+= 1
            print "Dataset swap number " + str(i)
            self.generateTrainSet()

            net.setDataset(self.trainSet)
            error = net.train()
            if(error > lasterror):
                net.saveNet("/home/osboxes/Documents/squaredImages/bigRotatedffnn.serialize")
                print "Saved!"
                lasterror = error

            print "Best successrate: " + str(lasterror)
            if(i==100): break



    def readData(self):
        datasN = DataGenerator.generateSampleDatabyFolder("/home/osboxes/Documents/squaredImages/new/_ano/", False)
        datasY = DataGenerator.generateSampleDatabyFolder("/home/osboxes/Documents/squaredImages/new/_crosswalks/", True)
        shuffle(datasY)
        shuffle(datasN)

        self.testsetCount = len(datasY)/4
        self.testSet = datasY[0:self.testsetCount] + datasN[0:self.testsetCount*2]

        self.dataY = datasY[self.testsetCount:len(datasY)-1]
        self.dataN = datasN[self.testsetCount*2:len(datasN)-1]
        self.generateTrainSet()


    def generateTrainSet(self):
        shuffle(self.dataN)
        self.trainSet = self.dataY + self.dataN[0:len(self.dataY)*2]
