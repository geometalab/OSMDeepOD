class Tile:
    def __init__(self):
        self.image = None
        self.bbox = None

    @classmethod
    def from_tile(cls, pil_image, bbox):
        tile = cls()
        tile.image = pil_image
        tile.bbox = bbox
        return tile

    def get_pixel(self, node):
        image_width = self.bbox.right - self.bbox.left
        image_height = self.bbox.top - self.bbox.bottom

        x = node.longitude - self.bbox.left
        y = node.latitude - self.bbox.bottom

        pixel_x =  int(self.image.size[0] * (x/image_width))
        pixel_y = self.image.size[1] - int(self.image.size[1] * (y/image_height))
        return (pixel_x, pixel_y)

    def show(self):
        self.image.show()