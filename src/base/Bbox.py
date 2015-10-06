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

    def toString(self):
       return str(self.left) + "," + str(self.bottom) + "," + str(self.right) + "," + str(self.top)

    def getDownLeftPoint(self):
        return Point(self.bottom,self.left)

    def getUpRightPoint(self):
        return Point(self.top,self.right)
