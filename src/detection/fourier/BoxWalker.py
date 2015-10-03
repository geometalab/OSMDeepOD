from service.ImagePlotter import ImagePlotter


class BoxWalker:
    def __init__(self, streetLoader, imageLoader):
        self.streetLoader = streetLoader
        self.imageLoader = imageLoader

    def walk(self, box):
        streets = self.streetLoader.getStreets(box)
        images = self.imageLoader.downloadImagesByPositions(box.getDownLeftPoint(), box.getUpRightPoint())
        ImagePlotter().plotMatrix(images)
