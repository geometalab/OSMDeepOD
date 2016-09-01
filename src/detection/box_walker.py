import datetime
import logging
from random import shuffle

from src.base.globalmaptiles import GlobalMercator
from src.base.search import Search
from src.data.fitting_bbox import FittingBbox
from src.data.node_merger import NodeMerger
from src.data.street_loader import StreetLoader
from src.data.tile_loader import TileLoader
from src.detection.street_walker import StreetWalker
from src.detection.tensor.detector import Detector
from src.data.osm_comparator import OsmComparator


class BoxWalker:
    def __init__(self, bbox, search=None):
        self.search = Search() if search is None else search
        self.bbox = FittingBbox(zoom_level=self.search.zoom_level).get(bbox)
        self.tile = None
        self.streets = []
        self.convnet = None
        self.logger = logging.getLogger(__name__)
        self.square_image_length = 50
        self.max_distance = self._calculate_max_distance(self.search.zoom_level, self.square_image_length)

    def load_convnet(self):
        self.convnet = Detector()
        if not self.search.word in self.convnet.labels:
            error_message = self.search.word + " is not in label file."
            self.logger.error(error_message)
            raise Exception(error_message)

    def load_tiles(self):
        self._printer("Start image loading.")
        loader = TileLoader(bbox=self.bbox, zoom_level=self.search.zoom_level)
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
        detected_nodes = []
        for i, _ in enumerate(tiles):
            prediction = predictions[i]
            if self.search.hit(prediction):
                detected_nodes.append(tiles[i].get_centre_node())
        self._printer("Stop detection.")
        merged_nodes = self._merge_near_nodes(detected_nodes)
        if self.search.compare:
            return self._compare_with_osm(merged_nodes)
        return merged_nodes

    def _get_tiles_of_box(self, streets, tile):
        street_walker = StreetWalker(tile=tile, square_image_length=self.square_image_length,
                                     zoom_level=self.search.zoom_level)
        tiles = []
        for street in streets:
            street_tiles = street_walker.get_tiles(street)
            tiles += street_tiles
        return tiles

    def _merge_near_nodes(self, node_list):
        merger = NodeMerger(node_list, self.max_distance)
        return merger.reduce()

    def _compare_with_osm(self, detected_nodes):
        comparator = OsmComparator(max_distance=self.max_distance)
        return comparator.compare(detected_nodes=detected_nodes, tag=self.search.tag, bbox=self.bbox)

    @staticmethod
    def _printer(message):
        print(str(datetime.datetime.now()) + ": " + message)

    @staticmethod
    def _calculate_max_distance(zoom_level, square_image_length):
        global_mercator = GlobalMercator()
        resolution = global_mercator.Resolution(zoom_level)
        return resolution * (square_image_length / 2)
