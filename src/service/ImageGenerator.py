import os
from service.ImageLoader import ImageLoader
from service.CrosswalkLoader import CrosswalkLoader
from PIL import Image

class ImageGenerator:

    def __init__(self, destinationPath):
        self.destinationPath = destinationPath

    def generate(self, downLeftPoint, upRightPoint):
        crosswalLoader = CrosswalkLoader()
        imageLoader = ImageLoader()
        crosswalks = crosswalLoader.getCrosswalksByPositions(downLeftPoint, upRightPoint)

        for crosswalk in crosswalks:
            image = imageLoader.download(crosswalk)
            image = image.crop((145, 145, 205, 205))
            self.__save(image, (str(crosswalk.latitude) + "_" + str(crosswalk.longitude)+".jpg"))


    def __save(self, image, filename):
        filepath = self.destinationPath + filename
        self.__removeIfExists(filepath)
        image.save(filepath)

    def __removeIfExists(self, filepath):
        if(os.path.exists(filepath)):
            os.remove(filepath)
