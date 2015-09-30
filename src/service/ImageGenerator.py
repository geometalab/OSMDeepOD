from PIL import Image
from geopy import Point
from service.ImageLoader import ImageLoader
from service.CrosswalkLoader import CrosswalkLoader

class ImageGenerator:

    def __init__(self, destinationPath):
        self.destinationPath = destinationPath

    def generate(self, downLeftPoint, upRightPoint):
        crosswalLoader = CrosswalkLoader()
        imageLoader = ImageLoader()
        crosswalks = crosswalLoader.getCrosswalksByPositions(downLeftPoint, upRightPoint)

        for crosswalk in crosswalks:
            image = imageLoader.download(crosswalk)
            image.crop((145, 205, 205, 145))
            self.__save(image, str(crosswalk.latitude) + "_" + str(crosswalk.longitude)+".jpg")



    def __save(self, image, name):
            image.save(self.destinationPath + name)
