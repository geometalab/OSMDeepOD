from Bbox import Bbox
from geopy.point import Point
from src.service.PositionHandler import PositionHandler


class Bbox19(Bbox):
    def __init__(self, left, bottom, zoomCorrection = 2):
        self.METER_PER_PIXEL = 0.404428571 / zoomCorrection #0.298 / zoomCorrection
        self.PIXEL_COUNT = 350 # 475
        self.DISTANCE = self.METER_PER_PIXEL * self.PIXEL_COUNT

        rightTop = self.__getRightTop(left, bottom)

        right = rightTop.longitude
        top = rightTop.latitude
        Bbox.__init__(self, left, bottom, right, top)

    def __getRightTop(self, left, bottom):
        leftDown = Point(bottom,left)
        handler = PositionHandler()
        return handler.addDistanceToPoint(leftDown, self.DISTANCE, self.DISTANCE)


    @staticmethod
    def toBbox19(bbox):
        bboxes19 = []
        y = bbox.bottom

        while(y < bbox.top):
            row = Bbox19.__convertRowTo19(bbox, y)
            bboxes19.append(row)
            y = row[0].top

        return bboxes19

    @staticmethod
    def __convertRowTo19(bbox , starty):
        results = []

        x = bbox.left
        while(x < bbox.right):
            bbox19 = Bbox19(x,starty)
            results.append(bbox19)
            x = bbox19.right

        return results





