import datetime
import logging
from random import shuffle

from src.detection.node_merger import NodeMerger
from src.detection.street_walker import StreetWalker
from src.data.tile_loader import TileLoader
from src.data.fitting_bbox import FittingBbox
from src.data.street_crosswalk_loader import StreetCrosswalkLoader
from src.detection.tensor.detector import Detector


class BoxWalker:
    def __init__(self, bbox):
        self.bbox = bbox
        self.tile = None
        self.streets = []
        self.osm_crosswalks = None
        self.convnet = None
        self.plain_result = None
        self.compared_with_osm_result = []
        self.logger = logging.getLogger(__name__)
        self.is_crosswalk_barrier = 0.98
        self.is_no_crosswalk_barrier = 0.1

    def load_convnet(self):
        self.convnet = Detector()

    def load_tiles(self):
        self._printer("Start image loading.")
        loader = TileLoader(self.bbox)
        loader.load_tile()
        self.tile = loader.tile
        self.bbox = self.tile.bbox
        self._printer("Stop image loading.")

    def load_streets(self):
        self._printer("Start street loading.")
        fitting_bbox = FittingBbox(bbox=self.bbox)
        bbox = fitting_bbox.get()
        if self.tile is None:
            self.logger.warning("Download tiles first")
        street_loader = StreetCrosswalkLoader()
        self.streets = street_loader.load_data(bbox)
        self.osm_crosswalks = street_loader.crosswalks
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
        tiles_count = len(tiles)
        self._printer(str(tiles_count) + " images to analise.")

        images = [tile.image for tile in tiles]
        predictions = self.convnet.detect(images)
        results = []
        for i in range(tiles_count):
            prediction = predictions[i]
            if self.is_crosswalk(prediction):
                results.append(tiles[i].get_centre_node())
        self.plain_result = self._merge_near_nodes(results)
        self.compared_with_osm_result = self._compare_osm_with_detected_crosswalks(self.plain_result)
        self._printer("Stop detection.")
        return self.compared_with_osm_result

    def is_crosswalk(self, prediction):
        return prediction['crosswalk'] > self.is_crosswalk_barrier \
               and prediction['noncrosswalk'] < self.is_no_crosswalk_barrier

    @staticmethod
    def _get_tiles_of_box(streets, tile):
        street_walker = StreetWalker(tile)
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

    def _compare_osm_with_detected_crosswalks(self, detected_crosswalks):
        result = []
        is_near = False
        DISTANCE_TO_CROSSWALK = 5.0
        for detected_crosswalk in detected_crosswalks:
            for osm_crosswalk in self.osm_crosswalks:
                if osm_crosswalk.get_distance_in_meter(
                        detected_crosswalk) < DISTANCE_TO_CROSSWALK:
                    is_near = True
                    break

            if not is_near:
                result.append(detected_crosswalk)
            is_near = False
        return result

    def _printer(self, message):
        print(str(datetime.datetime.now()) + ": " + message)
