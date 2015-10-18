from pybrain.structure import FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection
from pybrain.datasets import ClassificationDataSet
from pybrain.supervised.trainers import BackpropTrainer

import pickle

class NeuralNetwork:
    def __init__(self):
        self.nHidden1 = 50




    def initialize(self):
        n = FeedForwardNetwork()
        inLayer = LinearLayer(self.traindata.indim)
        n.addInputModule(inLayer)
        lastLayer = inLayer

        for i in range(0,3):
            layer = SigmoidLayer(self.nHidden1)
            n.addModule(layer)
            connection = FullConnection(lastLayer,layer)
            n.addConnection(connection)
            lastLayer = layer


        outLayer = LinearLayer(self.traindata.outdim)

        n.addOutputModule(outLayer)
        hidden_to_out = FullConnection(lastLayer, outLayer)
        n.addConnection(hidden_to_out)

        n.sortModules()
        self.net = n



    def setDataset(self, sampleDatas):
        self.sampleData = sampleDatas
        set = ClassificationDataSet(50*50,1, nb_classes=2)
        set.setField('class', [[0], [1]])
        for s in sampleDatas:
            inp = s.getNormalizedInputArray()
            outp = s.getOutputArray()
            set.addSample(inp, outp)

        set._convertToOneOfMany()
        self.dataset = set
        self.traindata = set

        print "Number of training patterns: ", len(self.traindata)
        print "Input and output dimensions: ", self.traindata.indim, self.traindata.outdim
        print "First sample (input, target, class):"
        print self.traindata['input'][0]
        print self.traindata['target'][0]
        #print self.traindata['class'][0]

    def setTestSet(self, sampleDatas):
        set = ClassificationDataSet(50*50,1, nb_classes=2)
        set.setField('class', [[0], [1]])
        for s in sampleDatas:
            inp = s.getNormalizedInputArray()
            outp = s.getOutputArray()
            set.addSample(inp, outp)

        set._convertToOneOfMany()
        self.testdata = set

    def train(self):
        trainer = BackpropTrainer(self.net, dataset=self.traindata, momentum=0.1, verbose=True, weightdecay=0.01)
        #trainer.trainUntilConvergence(dataset=self.traindata, maxEpochs=500,validationData=self.testdata)
        lastError = 0
        epoches = 20
        trainer.trainEpochs(epoches)

        error = self.printError()
        return error



    def printError(self):
        richtige = 0
        for s in self.testdata:
            ret = self.net.activate(s[0])
            crossWalkDetected = 0
            #if(ret[1] > 0.5): crossWalkDetected = 1
            if(ret[1] > 0.9 and ret[0] < 0.1): crossWalkDetected = 1

            print str(ret) + " Should: " + str(s[1][1]) + " Detected: " + str(crossWalkDetected)
            if(crossWalkDetected == s[1][1]): richtige += 1

        print "Erfolgsrate Testset: " + str((float(richtige) / len(self.testdata)) * 100)
        return (float(richtige) / len(self.testdata)) * 100

    def isCrosswalk(self, frequencies):
        ret = self.net.activate(frequencies)
        crosswalkDetected = ret[1] > 0.95 and ret[0] < 0.1
        if(crosswalkDetected): print ret
        return crosswalkDetected

    def saveNet(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(self.net, f)

    @staticmethod
    def fromFile(filepath):
        with open(filepath, 'rb') as f:
            net = pickle.load(f)
            neuralNetwork = NeuralNetwork()
            neuralNetwork.net = net
            return neuralNetwork