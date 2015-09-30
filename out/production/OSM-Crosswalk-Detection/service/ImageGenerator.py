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
        images = []

        left = 2407
        top = 804
        width = 300
        height = 200
        box = (left, top, left+width, top+height)
        area = img.crop(box)


        for crosswalk in crosswalks:
            image = imageLoader.download(crosswalk)
            w, h = image.size
            image.crop((0, 30, w, h-30))
            self.__save(image, str(crosswalk.latitude) + "_" + str(crosswalk.longitude))



    def __save(self, image, name):
            image.save(self.destinationPath + name)
