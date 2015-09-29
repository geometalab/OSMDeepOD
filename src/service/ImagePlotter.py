from matplotlib import pyplot as plt
from PIL import Image

class ImagePlotter:

    def __init__(self):
        pass

    def plotMatrix(self, images):
        numRows = len(images)
        numCols = len(images[0])
        width, height = images[0][0].size()

        result = Image.new("RGBA", (numCols * width, numRows * height))

        for x in range(0, numCols):
            for y in range(0, numRows):
                result.paste(images[x][y],(x * width, y * height))

        self.plot(result)


    def plot(self, image):
        plt.imshow(image)
        plt.show()
