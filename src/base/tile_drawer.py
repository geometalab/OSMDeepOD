from PIL import ImageDraw
from PIL.ImageShow import UnixViewer, register, quote, which


class XloadImageViewer(UnixViewer):
    @staticmethod
    def get_command_ex(the_file, title=None, **options):
        command = executable = "xloadimage"
        command += " -quiet "
        if title:
            command += " -title %s" % quote(title)
        return command, executable


if which("xloadimage"):
    register(XloadImageViewer)


class TileDrawer(object):
    def __init__(self):
        self.tile = None
        self.draw_section = None
        self.drawer = None

    @classmethod
    def from_tile(cls, tile):
        drawer = cls()
        drawer.tile = tile
        drawer.draw_section = tile.image.copy()
        drawer.drawer = ImageDraw.Draw(drawer.draw_section)
        return drawer

    def draw_point(self, node, point_size=6):
        (x, y) = self.tile.get_pixel(node)
        self.drawer.ellipse(
            (x - point_size, y - point_size, x + point_size, y + point_size),
            outline=(0, 255, 0),
            fill=(0, 255, 0))

    def draw_line(self, node1, node2, width=3):
        pixels1 = self.tile.get_pixel(node1)
        pixels2 = self.tile.get_pixel(node2)
        self.drawer.line([pixels1, pixels2], fill=(0, 0, 255), width=width)

    def draw_box(self, node, pixel_per_side):
        color = (255, 0, 0)
        half = pixel_per_side / 2

        pixels1 = self.tile.get_pixel(node)
        lb = (pixels1[0] - half, pixels1[1] - half)
        rb = (pixels1[0] - half, pixels1[1] + half)
        lt = (pixels1[0] + half, pixels1[1] - half)
        rt = (pixels1[0] + half, pixels1[1] + half)

        self.drawer.line([lb, rb], fill=color)
        self.drawer.line([rb, rt], fill=color)
        self.drawer.line([rt, lt], fill=color)
        self.drawer.line([lt, lb], fill=color)

    def show(self):
        self.draw_section.show()
