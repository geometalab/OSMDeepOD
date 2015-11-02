from src.data.StreetLoader import StreetLoader
from src.data.TileLoader import TileLoader

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

        streetloader = StreetLoader()
        drawer.streets = streetloader.load_streets(bbox)

        tileloader = TileLoader(bbox)
        drawer.tile = tileloader.get_big_tile()

        return drawer
    



