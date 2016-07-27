from ..data.street_crosswalk_loader import StreetCrosswalkLoader
from ..data.tile_loader import TileLoader
from ..base.tile_drawer import TileDrawer


class StreetDrawer(object):
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
    def from_bbox(cls, bbox, apiKey):
        drawer = cls()
        drawer.bbox = bbox

        tile_loader = TileLoader.from_bbox(bbox)
        tile_loader.load_tile()
        drawer.tile = tile_loader.tile
        street_loader = StreetCrosswalkLoader(api_key=apiKey)
        drawer.streets = street_loader.load_data(drawer.tile.bbox)

        return drawer

    def show(self):
        drawer = TileDrawer.from_tile(self.tile)
        for street in self.streets:
            drawer.draw_line(street.nodes[0], street.nodes[1])
        drawer.show()
