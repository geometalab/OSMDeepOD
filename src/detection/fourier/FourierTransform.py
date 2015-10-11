import cv2
from matplotlib import pyplot as plt
from scipy import ndimage
import numpy as np
from src.base.Tile import Tile


class FourierTransform:
    def __init__(self, tile, street):
        self.image = Tile.getCv2Image(tile.image)
        self.tile = tile
        self.street = street

        imgDimension = len(list(self.image))
        if(imgDimension > 2):
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY) #GrayScale


    def rotateImg(self):
        degree = self.street.getAngleDegree()
        self.image = ndimage.rotate(self.tile.image, -degree)

    def showImage(self):
        cv2.imshow('image',self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def getMiddleColumn(self):
        height = self.image.shape[0]
        width = self.image.shape[1]
        middle = width/2
        arr = np.array([], np.uint8)
        for y in range(0, height -1):
            arr = np.append(arr,[self.image[y,middle]])
        return arr

    def getFrequencies(self):
        column = self.getMiddleColumn()
        dft = np.fft.rfft(column)
        return dft

    def plotFrequencie(self):
        N = self.image.shape[0]
        yf = self.getFrequencies()
        xf = np.linspace(0.0, 1.0/(2.0), N/2)
        plt.plot(xf, 2.0/N * np.abs(yf[0:N/2]))
        plt.grid()
        plt.show()
        plt.imshow(self.image,aspect="auto")
        plt.show()

