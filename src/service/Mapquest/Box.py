from geopy import Point

class Box:
    def __init__(self):
        self.lat1 = "0"
        self.lon1 = "0"
        self.lat2 = "0"
        self.lon2 = "0"

    def __init__(self,lat1, lon1, lat2, lon2):
        self.lat1 = str(lat1)
        self.lon1 = str(lon1)
        self.lat2 = str(lat2)
        self.lon2 = str(lon2)

    def toString(self):
       return str(self.lon1) +"," + str(self.lat1) + "," + str(self.lon2) + ","  + str(self.lat2)

    def getDownLeftPoint(self):
        return Point(self.lat1,self.lon1)

    def getUpRightPoint(self):
        return Point(self.lat2,self.lon2)
