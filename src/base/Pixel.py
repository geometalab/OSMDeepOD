
class Pixel:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def toString(self):
        return 'x: ' + str(self.x) + ' y: ' + str(self.y)