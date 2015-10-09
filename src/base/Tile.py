import cv2
from PIL import Image
import numpy as np
from src.base.Bbox import Bbox
from matplotlib import pyplot as plt
from src.base.Node import Node
from src.service.PositionHandler import PositionHandler

class Tile:
    def __init__(self, image, bbox):
        self.image = image
        self.bbox = bbox
        self.isDrawing = False

    def startDrawing(self):
        self.drawImage = self.__getCv2Image(self.image)
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

    def __getCv2Image(self, pilimg):
       return cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)


    def __getPilImage(self, cv2img):
        cv2_im = cv2.cvtColor(cv2img,cv2.COLOR_BGR2RGB)
        return Image.fromarray(cv2_im)

    def getSquaredImages(self, node1, node2):
        PIXELCOUNT = 10
        METER_PER_PIXEL = 0.404428571
        stepDistance = PIXELCOUNT * METER_PER_PIXEL
        distanceBetweenNodes = node1.getDistanceInMeter(node2)

        squaresTiles = []
        for i in range(int(distanceBetweenNodes/stepDistance) +1):
            currentDistance = stepDistance * i
            currentNode = node1.stepTo(node2, currentDistance)

            tile =  self.__getSquaredImage(currentNode.toPoint())
            squaresTiles.append(tile)


        return squaresTiles

    def __getSquaredImage(self, centrePoint):
        PIXEL_PER_SIDE = 20
        METER_PER_PIXEL = 0.404428571
        DISTANCE = PIXEL_PER_SIDE * METER_PER_PIXEL

        centreNode = Node.create(centrePoint)
        leftDown = centreNode.addMeter(-DISTANCE/2,-DISTANCE/2)
        rightTop = centreNode.addMeter(DISTANCE/2,DISTANCE/2)

        box = Bbox()
        box.set(leftDown.toPoint(),rightTop.toPoint())

        return self.getSubTile(box)

    def getSubTile(self, bbox):
        cv2Image = self.__getCv2Image(self.image)

        p1 = self.getPixel(bbox.getDownLeftPoint())
        p2 = self.getPixel(bbox.getUpRightPoint())

        cropped = cv2Image[p2[1]:p1[1], p1[0]:p2[0]]
        cropped = self.__getPilImage(cropped)

        return Tile(cropped,bbox)

    def plot(self):
        plt.imshow(self.image)
        plt.show()