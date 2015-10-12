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
            #image = image.crop((145, 145, 205, 205)) #Image 60 x 60
            #image = image.crop((159, 159, 191, 191)) #Image 32 x 32
            #image = image.crop((155, 155, 195, 195)) #Image 40 x 40
            image = image.crop((165, 165, 185, 185)) #Image 20 x 20
            self.__save(image, (str(crosswalk.latitude) + "_" + str(crosswalk.longitude)+".jpg"))

    def generate(self, bbox):
        imageLoader = ImageLoader()
        images = imageLoader.downloadImagesByPositions(bbox)

        numRows = len(images)
        numCols = len(images[0])

        for i in range(0, numRows):
            for j in range(0, numCols):
                for x in range(0, 10):
                    for y in range(0, 10):
                        img = images[i][j].getImage().crop((x * 32, y * 32, (x + 1) * 32, (y + 1) * 32))
                        self.__save(img, (str(images[i][j].getPosition().latitude) + "_" + str(x) + str(y) + "_" + str(images[i][j].getPosition().longitude)+".jpg"))




    def __save(self, image, filename):
        filepath = self.destinationPath + filename
        self.__removeIfExists(filepath)
        image.save(filepath)

    def __removeIfExists(self, filepath):
        if(os.path.exists(filepath)):
            os.remove(filepath)
