import cv2
from PIL import Image
import numpy as np
from src.base.Bbox import Bbox
from matplotlib import pyplot as plt
from src.base.Node import Node
<<<<<<< HEAD
from geopy.point import Point
=======
from geopy import Point
from src.base.Constants import Constants
>>>>>>> master

class Tile:
    def __init__(self, image, bbox):
        self.image = image
        self.bbox = bbox
        self.isDrawing = False

    def startDrawing(self):
        self.drawImage = Tile.getCv2Image(self.image)
        self.isDrawing = True

    def stopDrawing(self):
        self.image = self.__getPilImage(self.drawImage)
        self.isDrawing = False

    def drawLine(self, point1, point2):
        if(not self.isDrawing): raise Exception("Enter startDrawing first")
        p1 = self.getPixel(point1)
        p2 = self.getPixel(point2)

        cv2.line(self.drawImage,p1,p2,(255,0,0),5)

    def getPixel(self, point):
        imagewidth = float(self.bbox.right) - float(self.bbox.left)
        imageheight = float(self.bbox.top) - float(self.bbox.bottom)

        x = point.longitude - float(self.bbox.left)
        y = point.latitude - float(self.bbox.bottom)

        pixelX =  int(self.image.size[0] * (x/imagewidth))
        pixelY = self.image.size[1] - int(self.image.size[1] * (y/imageheight))
        return (pixelX, pixelY)

    def getNode(self, pixel):
        x = pixel[0]
        y = pixel[1]
        xCount = self.image.size[0]
        yCount = self.image.size[1]
        yPart = (yCount - y) / float(yCount)
        xPart = x / float(xCount)

        latDiff = float(self.bbox.top) - float(self.bbox.bottom)
        lonDiff = float(self.bbox.right) - float(self.bbox.left)

        lat = float(self.bbox.bottom) + latDiff*yPart
        lon = float(self.bbox.left) + lonDiff*xPart

        return Node.create(Point(lat, lon))



    @staticmethod
    def getCv2Image(pilimg):
       return cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)


    def __getPilImage(self, cv2img):
        cv2_im = cv2.cvtColor(cv2img, cv2.COLOR_BGR2RGB)

        return Image.fromarray(cv2_im)

    def getSquaredImages(self, node1, node2):
        PIXELCOUNT = Constants.squaredImage_PixelPerSide / 3
        METER_PER_PIXEL = Constants.METER_PER_PIXEL
        stepDistance = PIXELCOUNT * METER_PER_PIXEL

        node1 = self.__ajustNodeToBoarder(node1)
        node2 = self.__ajustNodeToBoarder(node2)

        assert self.bbox.inBbox(node1.toPoint())
        assert self.bbox.inBbox(node2.toPoint())

        distanceBetweenNodes = node1.getDistanceInMeter(node2)

        squaresTiles = []
        for i in range(1, int(distanceBetweenNodes/stepDistance) + 1):
            currentDistance = stepDistance * i

            currentNode = node1.stepTo(node2, currentDistance)
            currentNode = self.__ajustNodeToBoarder(currentNode)

            assert self.bbox.inBbox(currentNode.toPoint())

            tile = self.__getSquaredImage(currentNode.toPoint())
            squaresTiles.append(tile)


        return squaresTiles

    def __ajustNodeToBoarder(self, node):
        xCount = self.image.size[0]
        yCount = self.image.size[1]
        pixel = self.getPixel(node.toPoint())
        resultPixel = [pixel[0], pixel[1]]

        borderPixel = Constants.squaredImage_PixelPerSide
        if(pixel[0] < borderPixel): resultPixel[0] = borderPixel
        if(pixel[1] < borderPixel): resultPixel[1] = borderPixel
        if(yCount - pixel[1] < borderPixel):
            resultPixel[1] = yCount - borderPixel
        if(xCount - pixel[0] < borderPixel):
            resultPixel[0] = xCount - borderPixel

        newnode = self.getNode(resultPixel)

        pixel2 = self.getPixel(newnode.toPoint())

        return newnode


    def __getSquaredImage(self, centrePoint):
        PIXEL_PER_SIDE = Constants.squaredImage_PixelPerSide
        METER_PER_PIXEL = Constants.METER_PER_PIXEL
        DISTANCE = PIXEL_PER_SIDE * METER_PER_PIXEL

        centreNode = Node.create(centrePoint)
        leftDown = centreNode.addMeter(-DISTANCE/2,-DISTANCE/2)
        rightTop = centreNode.addMeter(DISTANCE/2,DISTANCE/2)

        box = Bbox()
        box.set(leftDown.toPoint(),rightTop.toPoint())

        return self.getSubTile(box)

    def getSubTile(self, bbox):
        if(not(self.bbox.inBbox(bbox.getDownLeftPoint()) and self.bbox.inBbox(bbox.getUpRightPoint()))):
            raise Exception("given bbox is out of bbox of this tile")

        cv2Image = Tile.getCv2Image(self.image)

        p1 = self.getPixel(bbox.getDownLeftPoint())
        p2 = self.getPixel(bbox.getUpRightPoint())

        cropped = cv2Image[p2[1]:p1[1], p1[0]:p2[0]]

        assert cropped.size > 0


        cropped = self.__getPilImage(cropped)

        return Tile(cropped,bbox)

    def plot(self):
        plt.imshow(self.image)
        plt.show()