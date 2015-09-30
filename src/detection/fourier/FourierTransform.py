import cv2
from matplotlib import pyplot as plt
from scipy import ndimage
import numpy as np

class FourierTransform:
    def __init__(self, img):
        imgDimension = len(list(img.shape))
        if(imgDimension > 2):
            raise Exception("Use grayscaled images")
        self.img = img

    def rotateImg(self,degree):
        self.img = ndimage.rotate(self.img, degree)

    def showImage(self):
        cv2.imshow('image',self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def getMiddleColumn(self):
        height = self.img.shape[0]
        width = self.img.shape[1]
        middle = width/2
        arr = np.array([], np.uint8)
        for y in range(0, height -1):
            arr = np.append(arr,[self.img[y,middle]])
        return arr
    def getFrequencies(self):
        column = self.getMiddleColumn()
        dft = np.fft.rfft(column)
        return dft
    def plotFrequencie(self):
        N = self.img.shape[0]
        yf = self.getFrequencies()
        xf = np.linspace(0.0, 1.0/(2.0), N/2)
        plt.plot(xf, 2.0/N * np.abs(yf[0:N/2]))
        plt.grid()
        plt.show()

