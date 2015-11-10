import numpy as np
import cv2
from scipy import ndimage
from PIL import Image
from matplotlib import pyplot as plt
from src.base.Constants import Constants
import src.detection.deep.Convnet as Convnet
import cmath



class CrosswalkDetector:
    @classmethod
    def fromPilImage(cls, image, street):
        detector = cls()
        detector.pilimg = image
        detector.img = np.array(image)
        detector.cv2Image = cv2.cvtColor(detector.img, cv2.COLOR_RGB2GRAY)
        detector.street = street
        return detector

    @classmethod
    def fromSafedImageRotated(cls, image):
        detector = cls()
        img = np.array(image)
        detector.cv2Image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        detector.isNormalized = True
        return detector

    @staticmethod
    def predictCrosswalks(pilimg_list):
        x = np.zeros((len(pilimg_list), 50, 50, 3))

        for i in range(len(pilimg_list)):
            img = np.array(pilimg_list[i])
            x[i] = img
        x = x.reshape(x.shape[0], 3, 50, 50)

        results = Convnet.predict_list(x)
        return results

    @staticmethod
    def crop50(pilimg):
        size = 50
        (width, height) = pilimg.size
        x1 = width / 2 - size/2
        x2 = width / 2 + size/2
        y1 = height/2 + size/2
        y2 = height/2 - size/2

        return pilimg.crop((x1, y2, x2, y1))

    def __init__(self):
        self.street = None
        self.cv2Image = None
        self.isNormalized = False
        self.fourier2d = None
        self.absFourier2d = None
        self.img = None
        self.pilimg = None

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
        normalizeWith = 3000
        self.absFourier2d = []
        for y in range(0, len(self.fourier2d)):
            row = []
            for x in range(0, len(self.fourier2d[0])):
               absolute = abs(self.fourier2d[y, x]) / normalizeWith
               row.append(absolute)
            self.absFourier2d.append(row)

    def convertToPhase(self):
        normalizeWith = 3.2
        self.phaFourier2d = []
        for y in range(0, len(self.fourier2d)):
            row = []
            for x in range(0, len(self.fourier2d[0])):
               absolute = cmath.phase(self.fourier2d[y, x]) /normalizeWith
               row.append(absolute)
            self.phaFourier2d.append(row)


    def crop(self,pilimg):
        size = 50
        (width, height) = pilimg.size
        x1 = width / 2 - size/2
        x2 = width / 2 + size/2
        y1 = height/2 + size/2
        y2 = height/2 - size/2

        return pilimg.crop((x1, y2, x2, y1))

    def isCrosswalk2(self):
        if(self.pilimg.size[0] == 50 and self.pilimg.size[1] == 50):
            cropped = self.pilimg
        else:
            cropped = self.crop(self.pilimg)
        img = np.asarray(cropped)

        x = img.reshape(3, 50, 50)
        return Convnet.predict(x)

    def getPilImage(self):
        cv2_im = cv2.cvtColor(self.cv2Image, cv2.COLOR_GRAY2RGB)
        return Image.fromarray(cv2_im)

    def plot(self):
        plt.imshow(self.getPilImage())
        plt.show()