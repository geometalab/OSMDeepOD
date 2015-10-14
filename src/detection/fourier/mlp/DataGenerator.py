import glob
import Image
import string
from src.detection.fourier.FourierTransform import FourierTransform
from src.detection.fourier.mlp.SampleData import SampleData

class DataGenerator:
    def __init__(self, sourceFolder):
        self.sourceFolder = sourceFolder



    def generateSampleDatabyFolder(self):
        datas = []
        files = glob.glob(self.sourceFolder + "img*.png")

        for f in files:
            img = Image.open(f)
            transformer = FourierTransform(img)
            freq = transformer.calcFrequencies(0.5)
            sample = SampleData(freq, 0)
            datas.append(sample)

        return datas

    def generateSamplesByPixel(self):
        datas = []
        files = glob.glob(self.sourceFolder + "img*.png")

        for f in files:
            pixel = self.__getPixels(f)
            img = Image.open(f)
            transformer = FourierTransform(img)
            for x in range(pixel[0],pixel[1]):
                freq = transformer.calcFrequenciesByPixel(x)
                print pixel[0]
                #transformer.showImage()
                #transformer.plotFrequencie()
                sample = SampleData(freq, 1)
                datas.append(sample)


        return datas

    def __getPixels(self, path):
            x1 = 0
            x2 = 0
            path = string.replace(path,self.sourceFolder + "img","")
            path = string.replace(path,".png","")

            for i in range(0,len(path)):
                if(path[i] == ' '):
                    path = path[0:i]
                    break

            for i in range(0,len(path)):
                if(path[i] == '-'):
                    x1 = int(path[0:i])
                    x2 = int(path[i+1:len(path)])
                    break

            return (x1,x2)