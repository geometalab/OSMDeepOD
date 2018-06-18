from src.base.node import Node
from src.detection.walker import Walker
from src.data.osm.overpass_api import OverpassApi


class OsmObjectWalker(Walker):
    def __init__(self, tile, tags, square_image_length=50, zoom_level=19, step_width=0.66):
        super(OsmObjectWalker, self).__init__(tile, square_image_length, zoom_level, step_width)
        self.tags = tags

    def get_tiles(self):
        nodes = self._calculate_tile_centres()
        squared_tiles = self._get_squared_tiles(nodes)
        return squared_tiles

    def _calculate_tile_centres(self):
        centers = []

        # [out:csv(::lat,::lon)][timeout:25];node["public_transport"="platform"]({{bbox}});out;
        self.api = OverpassApi()
        data = self.api.get(self.tile.bbox, self.tags, nodes=True, ways=False, relations=False, responseformat='csv(::lat,::lon)')
        data = list(map(lambda cc: Node(float(cc[0]), float(cc[1])), data[1:]))
        print(data)

        return data
