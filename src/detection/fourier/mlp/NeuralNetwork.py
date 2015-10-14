from pybrain.structure import FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import ClassificationDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer
from pybrain.utilities import percentError
import pickle

class NeuralNetwork:
    def __init__(self):
        self.nHidden1 = 50
        self.nHidden2 = self.nHidden1


    def initialize(self):
        n = FeedForwardNetwork()
        inLayer = LinearLayer(self.traindata.indim)
        hiddenLayer = SigmoidLayer(self.nHidden1)
        hiddenLayer2 = SigmoidLayer(self.nHidden2)
        outLayer = LinearLayer(self.traindata.outdim)
        n.addInputModule(inLayer)
        n.addModule(hiddenLayer)
        n.addModule(hiddenLayer2)
        n.addOutputModule(outLayer)
        in_to_hidden = FullConnection(inLayer, hiddenLayer)
        hidden_to_hidden = FullConnection(hiddenLayer, hiddenLayer2)
        hidden_to_out = FullConnection(hiddenLayer2, outLayer)
        n.addConnection(in_to_hidden)
        n.addConnection(hidden_to_hidden)
        n.addConnection(hidden_to_out)
        n.sortModules()
        return n



    def setDataset(self, sampleDatas):
        self.sampleData = sampleDatas
        set = ClassificationDataSet(20,1, nb_classes=2)
        set.setField('class', [[0], [1]])
        for s in sampleDatas:
            set.addSample(s.input, [s.isCrosswalk])

        set._convertToOneOfMany()
        self.dataset = set
        self.testdata, self.traindata = set.splitWithProportion(0.25) #Split set into train (75%) and test (25%)


        print "Number of training patterns: ", len(self.traindata)
        print "Input and output dimensions: ", self.traindata.indim, self.traindata.outdim
        print "First sample (input, target, class):"
        print self.traindata['input'][0]
        print self.traindata['target'][0]
        #print self.traindata['class'][0]

    def train(self):
        trainer = BackpropTrainer(self.net, dataset=self.traindata, momentum=0.1, verbose=True, weightdecay=0.01)
        #trainer.trainUntilConvergence(dataset=self.traindata, maxEpochs=500,validationData=self.testdata)

        epoches = 200
        for i in range(epoches/5):
            trainer.trainEpochs(5)
            print str(i*5)

        self.printError()
        self.saveNet("/home/osboxes/Documents/squaredImages/ffnn.serialize")

    def printError(self):
        richtige = 0

        for s in self.testdata:
            ret = self.net.activate(s[0])
            crossWalkDetected = 0
            if(ret[1] > 0.5): crossWalkDetected = 1
            print str(ret) + " Should: " + str(s[1][1]) + " Detected: " + str(crossWalkDetected)
            if(crossWalkDetected == s[1][1]): richtige += 1

        print "Erfolgsrate: " + str((float(richtige) / len(self.testdata)) * 100)

    def saveNet(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(self.net, f)

    @staticmethod
    def fromFile(filepath):
        with open(filepath, 'rb') as f:
            net = pickle.load(f)
            return net