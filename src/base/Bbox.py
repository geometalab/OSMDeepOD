from geopy import Point

class Bbox:
    def __init__(self):
        self.bottom = "0"
        self.left = "0"
        self.top = "0"
        self.right = "0"

    def __init__(self,left, bottom, right, top):
        self.bottom = str(bottom)
        self.left = str(left)
        self.top = str(top)
        self.right = str(right)
        if(not self.__isValid()): raise Exception("Cordinates are not valid")

    def __isValid(self):
        return float(self.bottom) < float(self.top) and float(self.left) < float(self.right)

    def toString(self):
       return str(self.bottom) + "," + str(self.right) + "," + str(self.top)  + "," + str(self.left)

    def getMapquestFormat(self):
        return   str(self.left) + "," + str(self.bottom) + "," + str(self.right) + "," + str(self.top)

    def getBingFormat(self):
        return str(self.bottom) + "," + str(self.left) + "," + str(self.top)  + "," + str(self.right)

    def printing(self):
        return "Bottom: " + str(self.bottom) + ", Right: " + str(self.right) + ", Top: " + str(self.top)  + ", Left: " + str(self.left)

    def getDownLeftPoint(self):
        return Point(self.bottom,self.left)

    def getUpRightPoint(self):
        return Point(self.top,self.right)

    def inBbox(self, point):
        lat = point.latitude
        lon = point.longitude

        inLat = lat >= float(self.bottom) and lat <= float(self.top)
        intLon = lon >= float(self.left) and lon <= float(self.right)

        return inLat and intLon


