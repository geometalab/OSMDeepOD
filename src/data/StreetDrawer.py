from src.data.StreetCrosswalkLoader import StreetCrosswalkLoader
from src.data.TileLoader import TileLoader
from src.base.TileDrawer import TileDrawer


class StreetDrawer:

    def __init__(self):
        self.streets = None
        self.tile = None
        self.bbox = None

    @classmethod
    def from_streets_tile(cls, streets, tile):
        drawer = cls()
        drawer.streets = streets
        drawer.tile = tile
        drawer.bbox = tile.bbox
        return drawer

    @classmethod
    def from_bbox(cls, bbox):
        drawer = cls()
        drawer.bbox = bbox

        tileloader = TileLoader.from_bbox(bbox)
        tileloader.load_tile()
        drawer.tile = tileloader.tile
        streetloader = StreetCrosswalkLoader()
        drawer.streets = streetloader.load_data(drawer.tile.bbox)

        return drawer

    def show(self):
        drawer = TileDrawer.from_tile(self.tile)
        for street in self.streets:
            drawer.draw_line(street.nodes[0], street.nodes[1])
        drawer.show()
