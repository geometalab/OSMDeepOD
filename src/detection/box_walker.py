import datetime
import logging
from random import shuffle

from src.base.search import Search
from src.data.fitting_bbox import FittingBbox
from src.data.node_loader import NodeLoader
from src.data.node_merger import NodeMerger
from src.data.street_loader import StreetLoader
from src.data.tile_loader import TileLoader
from src.detection.street_walker import StreetWalker
from src.detection.tensor.detector import Detector


class BoxWalker:
    def __init__(self, bbox, zoom_level=19, search=Search()):
        self.bbox = FittingBbox(zoom_level=zoom_level).get(bbox)
        self.zoom_level = zoom_level
        self.tile = None
        self.streets = []
        self.search_nodes = []
        self.convnet = None
        self.logger = logging.getLogger(__name__)
        self.search = search
        self.square_image_length = 50

    def load_convnet(self):
        self.convnet = Detector()

    def load_tiles(self):
        self._printer("Start image loading.")
        loader = TileLoader(bbox=self.bbox, zoom_level=self.zoom_level)
        loader.load_tile()
        self.tile = loader.tile
        self._printer("Stop image loading.")

    def load_streets(self):
        self._printer("Start street loading.")
        if self.tile is None:
            self.logger.warning("Download tiles first")
        street_loader = StreetLoader()
        self.streets = street_loader.load_data(self.bbox)
        shuffle(self.streets)
        self._printer("Stop street loading.")

    def load_search_nodes(self):
        self._printer("Start node loading.")
        node_loader = NodeLoader()
        self.search_nodes = node_loader.load_data(self.bbox, self.search.tag)
        self._printer("Stop node loading.")

    def walk(self):
        ready_for_walk = (not self.tile is None) and (
            not self.streets is None) and (
                             not self.convnet is None)
        if not ready_for_walk:
            error_message = "Not ready for walk. Load tiles, streets and convnet first"
            self.logger.error(error_message)
            raise Exception(error_message)

        self._printer("Start detection.")
        tiles = self._get_tiles_of_box(self.streets, self.tile)
        self._printer(str(len(tiles)) + " images to analyze.")

        images = [tile.image for tile in tiles]
        predictions = self.convnet.detect(images)
        results = []
        for i, _ in enumerate(tiles):
            prediction = predictions[i]
            if self.search.hit(prediction):
                results.append(tiles[i].get_centre_node())
        self._printer("Stop detection.")
        return self._merge_near_nodes(results)

    def _get_tiles_of_box(self, streets, tile):
        street_walker = StreetWalker(tile=tile, square_image_length=self.square_image_length,
                                     zoom_level=self.zoom_level)
        tiles = []
        for street in streets:
            street_tiles = street_walker.get_tiles(street)
            tiles += street_tiles
        return tiles

    @staticmethod
    def _merge_near_nodes(nodelist):
        merger = NodeMerger.from_nodelist(nodelist)
        merger.max_distance = 7
        return merger.reduce()

    def _printer(self, message):
        print(str(datetime.datetime.now()) + ": " + message)
