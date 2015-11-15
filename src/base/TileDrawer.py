from src.base.Tile import Tile
import Image, ImageDraw
class TileDrawer:
    def __init__(self):
        self.tile = None
        self.drawsection = None
        self.drawer = None

    @classmethod
    def from_tile(cls, tile):
        drawer = cls()
        drawer.tile = tile
        drawer.drawsection = tile.image.copy()
        drawer.drawer = ImageDraw.Draw(drawer.drawsection)
        return drawer

    def draw_point(self, node, pointsize=6):
        (x, y) = self.tile.get_pixel(node)
        self.drawer.ellipse((x-pointsize, y-pointsize, x+pointsize, y+pointsize), outline=(0,255,0), fill=(0,255,0))

    def draw_line(self, node1, node2, width=3):
        pixels1 = self.tile.get_pixel(node1)
        pixels2 = self.tile.get_pixel(node2)
        self.drawer.line([pixels1,pixels2], fill=(0,0,255), width=width)

    def draw_box(self, node, pixel_per_side):
        color = (255,0,0)
        half = pixel_per_side/2

        pixels1 = self.tile.get_pixel(node)
        lb = (pixels1[0] - half,pixels1[1] - half)
        rb = (pixels1[0] - half,pixels1[1] + half)
        lt = (pixels1[0] + half,pixels1[1] - half)
        rt = (pixels1[0] + half,pixels1[1] + half)

        self.drawer.line([lb,rb], fill=color)
        self.drawer.line([rb,rt], fill=color)
        self.drawer.line([rt,lt], fill=color)
        self.drawer.line([lt,lb], fill=color)

    def show(self):
        self.drawsection.show()

