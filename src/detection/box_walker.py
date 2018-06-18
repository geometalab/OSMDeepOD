import datetime
import logging
import threading
import queue

from importlib import import_module
from itertools import chain

from src.base.globalmaptiles import GlobalMercator
from src.base.configuration import Configuration
from src.base.tag import Tag
from src.base.tile import Tile
from src.data.osm.node_merger import NodeMerger
from src.data.osm.osm_comparator import OsmComparator
from src.data.osm.street_loader import StreetLoader
from src.detection.street_walker import StreetWalker
from src.detection.tensor.detector import Detector
from src.detection.tile_walker import TileWalker

logger = logging.getLogger(__name__)


class BackgroundGenerator(threading.Thread):
    def __init__(self, generator, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.generator = generator
        self.daemon = True
        #self.start()

    def run(self):
        for item in self.generator:
            print("put: " + str(self.queue.qsize()))
            self.queue.put(item)
        self.queue.put(None)

    def __iter__(self):
        return self

    def __next__(self):
        print("next: " + str(self.queue.qsize()))
        next_item = self.queue.get()
        if next_item is None:
             raise StopIteration
        return next_item


class BackgroundGeneratorPool:
    def __init__(self, generator, n=8):
        q = queue.Queue(100)
        self.pool = list(map(lambda _: BackgroundGenerator(generator, q), range(n)))
        for b in self.pool:
            b.start()

    def __iter__(self):
        return self.pool[0].__iter__()

    def __next__(self):
        return self.pool[0].__next__()


class BoxWalker:
    def __init__(self, bbox, configuration=None):
        self.configuration = Configuration() if configuration is None else configuration
        self.bbox = bbox
        self.streets = []
        self.convnet = None
        self.square_image_length = 100
        self.max_distance = self._calculate_max_distance(self.configuration.DETECTION.zoomlevel,
                                                         self.square_image_length)
        self.image_api = self._get_image_api(self.configuration.DETECTION.orthophoto)
        self.tile = Tile(image_api=self.image_api, bbox=self.bbox)

    @staticmethod
    def _get_image_api(image_api):
        source = 'src.data.orthofoto.' + image_api + '.' + image_api + '_api'
        module = import_module(source)
        class_ = getattr(module, image_api.title() + 'Api')
        return class_()

    def load_convnet(self):
        self.convnet = Detector(labels_file=self.configuration.DETECTION.labels,
                                graph_file=self.configuration.DETECTION.network)
        if not self.configuration.DETECTION.word in self.convnet.labels:
            error_message = self.configuration.DETECTION.word + " is not in label file."
            logger.error(error_message)
            raise Exception(error_message)

    def load_streets(self):
        self._printer("Start street loading.")
        street_loader = StreetLoader()
        self.streets = street_loader.load_data(self.bbox)
        self._printer(str(len(self.streets)) + " streets to walk.")
        self._printer("Stop street loading.")

    def walk(self):
        ready_for_walk = not self.convnet is None
        if not ready_for_walk:
            error_message = "Not ready for walk. Load tiles and convnet first"
            logger.error(error_message)
            raise Exception(error_message)

        self._printer("Start detection.")

        follow_streets = self.configuration.to_bool(self.configuration.DETECTION.followstreets)

        if follow_streets:
            tiles = self._get_tiles_of_box_with_streets(self.streets, self.tile)
        else:
            tiles = self._get_tiles_of_box(self.tile)

        #self._printer("{0} images to analyze.".format(str(len(tiles))))

        tiles = BackgroundGeneratorPool(tiles, n=32) # Fetch next images while running detect
        predictions = self.convnet.detect(tiles)
        detected_nodes = []
        for prediction in predictions:
            if self.hit(prediction):
                detected_nodes.append(prediction['tile'].get_centre_node())
        self._printer("Stop detection.")
        merged_nodes = self._merge_near_nodes(detected_nodes)

        compare = self.configuration.to_bool(self.configuration.DETECTION.compare)
        print('Compare with OpenStreetMap entries: {0}'.format(compare))
        if compare:
            return self._compare_with_osm(merged_nodes)
        return merged_nodes

    def _get_tiles_of_box(self, tile):
        tile_walker = TileWalker(tile=tile, square_image_length=self.square_image_length,
                                 zoom_level=self.configuration.DETECTION.zoomlevel,
                                 step_width=self.configuration.DETECTION.stepwidth)
        tiles = tile_walker.get_tiles()
        return tiles

    def _get_tiles_of_box_with_streets(self, streets, tile):
        street_walker = StreetWalker(tile=tile, square_image_length=self.square_image_length,
                                     zoom_level=self.configuration.DETECTION.zoomlevel,
                                     step_width=self.configuration.DETECTION.stepwidth)

        return chain.from_iterable(map(street_walker.get_tiles, streets))


    def _merge_near_nodes(self, node_list):
        merger = NodeMerger(node_list, self.max_distance)
        return merger.reduce()

    def _compare_with_osm(self, detected_nodes):
        comparator = OsmComparator(max_distance=self.max_distance)
        tag = Tag(key=self.configuration.DETECTION.key, value=self.configuration.DETECTION.value)
        return comparator.compare(detected_nodes=detected_nodes, tag=tag, bbox=self.bbox)

    def hit(self, prediction):
        return prediction[self.configuration.DETECTION.word] > float(self.configuration.DETECTION.barrier)

    @staticmethod
    def _printer(message):
        print("{0}: {1}".format(str(datetime.datetime.now()), message))

    @staticmethod
    def _calculate_max_distance(zoom_level, square_image_length):
        global_mercator = GlobalMercator()
        resolution = global_mercator.Resolution(zoom_level)
        return resolution * (square_image_length / 2)
