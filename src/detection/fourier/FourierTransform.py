import cv2
from matplotlib import pyplot as plt
from scipy import ndimage
import numpy as np
from src.base.Tile import Tile
from PIL import Image
import cmath


class FourierTransform:
    def __init__(self, tile, street):
        self.image = Tile.getCv2Image(tile.image)
        self.tile = tile
        self.street = street

        imgDimension = len(list(self.image))
        if(imgDimension > 2):
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY) #GrayScale

    def normalizeImage(self):
        equ = cv2.equalizeHist(self.image)
        self.image = equ

    def rotateImg(self):
        degree = self.street.getAngleDegree()
        img = self.getPilImage(self.image)
        img = ndimage.rotate(img, -degree)
        self.image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    def getPilImage(self, cv2img):
        cv2_im = cv2.cvtColor(cv2img, cv2.COLOR_GRAY2RGB)

        return Image.fromarray(cv2_im)

    def showImage(self):
        img = self.getPilImage(self.image)
        plt.imshow(img)
        plt.show()


    def __getColumn(self, where0to1):
        height = self.image.shape[0]
        width = self.image.shape[1]
        middle = width* where0to1
        middle = int(middle)
        arr = np.array([], np.uint8)
        for y in range(0, height -1):
            arr = np.append(arr,[self.image[y,middle]])
        return arr

    def isZebra(self):
        trigger = 1000
        cuts = 6
        for i in range(1,cuts):
            onePart = 1/(float(cuts) + 1)
            where0to1 = onePart * i
            frequencies = self.__calcFrequencies(where0to1)
            isZebra = frequencies[11] > trigger
            if(isZebra): return True

        return False

    def __calcFrequencies(self, where0to1):
        column = self.__getColumn(where0to1)
        dft = np.fft.rfft(column)
        dtf = dft[0:20]
        absolut = []
        for x in dtf:
            absolut.append(abs(x))
        return absolut



    def printFrequencie(self):
        yf = self.getFrequencies()
        absolut = []

        for x in yf:
            absolut.append(abs(x))

        print ""
        print "Abs 11: " + str(absolut[11]) + " 9: " + str(absolut[9]) + " 10: " + str(absolut[10])


        #print "-------Phase 7: " + str(cmath.phase(yf[7])) + " 8: " + str(cmath.phase(yf[8])) + " 9: " + str(cmath.phase(yf[9]))
    def plotFrequencie(self):
        yf = self.getFrequencies()
        absolut = []

        for x in yf:
            absolut.append(abs(x))

        for i in range(0, 4):
            absolut[i] = 0
        plt.plot(absolut)
        plt.show()

