import glob
import Image
from src.detection.fourier.CrosswalkDetector import CrosswalkDetector
from src.detection.fourier.mlp.SampleData import SampleData
import PIL
import matplotlib.pyplot as plt

class DataGenerator:
    @staticmethod
    def generateSampleDatabyFolder(folderPath, isCrosswalk = False):
        datas = []
        files = glob.glob(folderPath + "img*.png")

        for f in files:
            img = Image.open(f)
            sizeOk = img.size[0] == 50 and img.size[1] == 50
            assert sizeOk
            detector = CrosswalkDetector.fromSafedImageRotated(img)
            detector.calc2dFourier()
            detector.convertToAbsolute()
            sample = SampleData.fromAbsoluteFourier2d(detector.absFourier2d, isCrosswalk)
            datas.append(sample)

        return datas
