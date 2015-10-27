from matplotlib import pyplot as plt
from PIL import Image


class ImagePlotter:

    def __init__(self):
        pass

    def plotMatrix(self, images):
        numRows = len(images)
        numCols = len(images[0])
        width, height = images[0][0].getImage().size

        result = Image.new("RGBA", (numCols * width, numRows * height))

        for y in range(0, numRows):
            for x in range(0, numCols):
                result.paste(images[y][x].getImage(),(x * width, (numRows -1 -y) * height))

        self.plot(result)

    def plotTileMatrix(self, tiles):
        numRows = len(tiles)
        numCols = len(tiles[0])
        print tiles[0][0]
        width, height = tiles[0][0].image.size

        result = Image.new("RGBA", (numCols * width, numRows * height))

        for y in range(0, numRows):
            for x in range(0, numCols):
                result.paste(tiles[y][x].image,(x * width, (numRows -1 -y) * height))

        self.plot(result)

    def plotGoogleTileMatrix(self, tiles):
        numRows = len(tiles)
        numCols = len(tiles[0])
        width, height = tiles[0][0].image.size

        result = Image.new("RGBA", (numCols * width, numRows * height))

        for y in range(0, numRows):
            for x in range(0, numCols):
                result.paste(tiles[y][x].image,(x * width, y * height))

        self.plot(result)

    def plotImageListInLon(self, images):
        width, height = images[0].size

        result = Image.new("RGBA", (len(images) * width, height))

        for i in range(0, len(images)):
            result.paste(images[i],(i * width,0 ))

        self.plot(result)

    def plotImageListInLat(self, images):
        width, height = images[0].size

        result = Image.new("RGBA", (width, len(images) * height))

        for i in range(0, len(images)):
            result.paste(images[len(images)-1 -i],(0, i * height))

        self.plot(result)


    def plot(self, image):
        plt.imshow(image)
        plt.show()