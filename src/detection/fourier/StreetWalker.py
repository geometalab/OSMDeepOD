from service.ImagePlotter import ImagePlotter

class StreetWalker:
    def __init__(self, street, images):
        self.street = street
        self.images = images

    def walk(self):
        print "walk"
