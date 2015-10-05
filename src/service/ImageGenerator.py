import os
from src.service.ImageLoader import ImageLoader
from src.service.CrosswalkLoader import CrosswalkLoader

class ImageGenerator:

    def __init__(self, destinationPath):
        self.destinationPath = destinationPath

    def generateCrosswalks(self, bbox):
        crosswalLoader = CrosswalkLoader()
        imageLoader = ImageLoader()
        crosswalks = crosswalLoader.getCrosswalksByPositions(bbox)

        for crosswalk in crosswalks:
            image = imageLoader.download(crosswalk)
            image = image.crop((145, 145, 205, 205))
            self.__save(image, (str(crosswalk.latitude) + "_" + str(crosswalk.longitude)+".jpg"))

    def generate(self, bbox):
        imageLoader = ImageLoader()
        images = imageLoader.downloadImagesByPositions(bbox)

        numRows = len(images)
        numCols = len(images[0])

        for i in range(0, numRows):
            for j in range(0, numCols):
                for x in range(0, 5):
                    for y in range(0, 5):
                        img = images[i][j].getImage().crop((x * 60, y * 60, (x + 1) * 60, (y + 1) * 60))
                        self.__save(img, (str(images[i][j].getPosition().latitude) + "_" + str(x) + str(y) + "_" + str(images[i][j].getPosition().longitude)+".jpg"))




    def __save(self, image, filename):
        filepath = self.destinationPath + filename
        self.__removeIfExists(filepath)
        image.save(filepath)

    def __removeIfExists(self, filepath):
        if(os.path.exists(filepath)):
            os.remove(filepath)
