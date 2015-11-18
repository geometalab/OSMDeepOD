from src.data.StreetLoader import StreetLoader
from src.data.TileLoader import TileLoader
from src.base.TileDrawer import TileDrawer

class StreetDrawer:
    def __init(self):
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



        tileloader = TileLoader(bbox)
        drawer.tile = tileloader.load_tile()
        streetloader = StreetLoader()
        drawer.streets = streetloader.load_streets(drawer.tile.bbox)

        return drawer

    def show(self):
        drawer = TileDrawer.from_tile(self.tile)
        for street in self.streets:
            drawer.draw_line(street.nodes[0], street.nodes[1])
        drawer.show()




