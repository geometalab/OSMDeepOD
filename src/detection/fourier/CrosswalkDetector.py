import numpy as np
import cv2
from src.detection.fourier.mlp.NeuralNetwork import NeuralNetwork
from src.detection.fourier.mlp.SampleData import SampleData
import PIL
from scipy import ndimage
from PIL import Image
from matplotlib import pyplot as plt
from src.base.Constants import Constants


class CrosswalkDetector:
    @classmethod
    def fromPilImage(cls, image, street):
        detector = cls()
        img = np.array(image)
        detector.cv2Image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        detector.street = street
        return detector

    @classmethod
    def fromSafedImageRotated(cls, image):
        detector = cls()
        img = np.array(image)
        detector.cv2Image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        detector.isNormalized = True
        return detector



    def __init__(self):
        self.street = None
        self.cv2Image = None
        self.isNormalized = False
        self.fourier2d = None
        self.absFourier2d = None

    def process(self):
        self.rotateImg()
        self.cut()
        self.normalize()
        self.calc2dFourier()
        self.convertToAbsolute()

    def normalize(self):
        equ = cv2.equalizeHist(self.cv2Image)
        self.cv2Image = equ
        self.isNormalized = True

    def rotateImg(self):
        degree = self.street.getAngleDegree()
        self.cv2Image = ndimage.rotate(self.cv2Image,-degree)

    def cut(self):
        middlex = self.cv2Image.shape[1]/2
        middley = self.cv2Image.shape[0]/2

        x1 = middlex - Constants.squaredImage_PixelPerSide/2
        x2 = middlex + Constants.squaredImage_PixelPerSide/2

        y1 = middley - Constants.squaredImage_PixelPerSide/2
        y2 = middley + Constants.squaredImage_PixelPerSide/2

        p1 = (x1, y2)
        p2 = (x2, y1)

        cropped = self.cv2Image[p2[1]:p1[1], p1[0]:p2[0]]

        assert cropped.size > 0
        sizeOk = cropped.shape[0] == 50 and cropped.shape[1] == 50
        if(not sizeOk):
            print""
        self.cv2Image = cropped

    def calc2dFourier(self):
        if(not self.isNormalized): raise Exception("Normalize image first")

        four2d = np.fft.fft2(self.cv2Image)
        self.fourier2d = four2d

    def convertToAbsolute(self):
        self.absFourier2d = []
        for y in range(0, len(self.fourier2d)):
            row = []
            for x in range(0, len(self.fourier2d[0])):
               absolute = abs(self.fourier2d[y, x])
               row.append(absolute)
            self.absFourier2d.append(row)

    def isCrosswalk(self):
        data = SampleData.fromAbsoluteFourier2d(self.absFourier2d)
        inputVector = data.getNormalizedInputArray()
        net = CrosswalkDetector.getNeuralNetwork()
        assert len(inputVector) == 2500
        res = net.isCrosswalk(inputVector)
        return res
    def getPilImage(self):
        cv2_im = cv2.cvtColor(self.cv2Image, cv2.COLOR_GRAY2RGB)
        return Image.fromarray(cv2_im)

    def plot(self):
        plt.imshow(self.getPilImage())
        plt.show()

    neuralNetwork = None
    @staticmethod
    def getNeuralNetwork():
        if(CrosswalkDetector.neuralNetwork is None):

            #CrosswalkDetector.neuralNetwork = NeuralNetwork.fromFile("/home/osboxes/Documents/squaredImages/ffnn50,50,85.7 2d.serialize")
            CrosswalkDetector.neuralNetwork = NeuralNetwork.fromFile("/home/osboxes/Documents/squaredImages/bigRotatedffnn,80,80,90% (fast bester - min 0.95! -).serialize")
        return CrosswalkDetector.neuralNetwork



