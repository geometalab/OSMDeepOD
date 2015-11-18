from src.detection.StreetWalker import StreetWalker
from src.data.TileLoader import TileLoader
from src.data.StreetLoader import StreetLoader
import datetime
import src.detection.deep.Convnet as Convnet
from src.detection.NodeMerger import NodeMerger
from random import shuffle


class BoxWalker:
    def __init__(self, bbox, verbose=True):
        self.bbox = bbox
        self.tile = None
        self.verbose = verbose
        self.status_printer = StatusPrinter.from_nb_streets(verbose)

    def load_convnet(self):
        Convnet.initialize()

    def load_tiles(self):
        self.status_printer.start_load_tiles()

        loader = TileLoader.from_bbox(self.bbox, self.verbose)
        self.tile = loader.load_tile()
        self.bbox = self.tile.bbox

    def load_streets(self):
        self.status_printer.start_load_streets()

        streetLoader = StreetLoader()
        self.streets = streetLoader.load_streets(self.bbox)
        shuffle(self.streets)
        self.status_printer.set_nb_streets(len(self.streets))

    def walk(self):
        self.status_printer.start_walking()

        results = []
        nb_images = 0

        for i in range(len(self.streets)):
            street = self.streets[i]
            streetwalker = StreetWalker.from_street_tile(street, self.tile)
            street_results = streetwalker.walk()
            results += street_results
            nb_images += streetwalker.nb_images
            self.status_printer.set_state(i,len(results))

        self.status_printer.end_walking(nb_images)

        return self._merge_near_nodes(results)

    def _merge_near_nodes(self, nodelist):
        merger = NodeMerger.from_nodelist(nodelist)
        return merger.reduce()


class StatusPrinter:
    def __init__(self):
        self.nb_streets = 0
        self.last_percentage = 0.0
        self.start_time = None
        self.end_time = None
        self.verbose = True

    @classmethod
    def from_nb_streets(cls, verbose=True):
        printer = cls()
        printer.verbose = verbose
        return printer

    def start_load_tiles(self):
        self._out("Loading images within bounding box", True)

    def start_load_streets(self):
        self._out("Loading streets within bounding box", True)

    def set_nb_streets(self, nb_streets):
        self.nb_streets = nb_streets
        self._out(str(self.nb_streets) + " streets loaded")

    def start_walking(self):
        self.start_time = datetime.datetime.now()
        self._out("Start Walking", True)

    def end_walking(self, nb_images):
        self.end_time = datetime.datetime.now()
        self._out("End Walking", True)
        self._out("Time needed: " + str((self.end_time - self.start_time).seconds) + " seconds")
        self._out(str(nb_images) + " images predicted")

    def set_state(self, nb_streets_done, nb_detected_crosswalks):
        current_percentage = (nb_streets_done / float(self.nb_streets)) * 100

        if self.last_percentage + 1 < current_percentage:
            self.last_percentage = current_percentage
            remaing_time = self._calc_remaining_duration(self.last_percentage)
            msg = str(int(current_percentage)) + "% - " + str(nb_detected_crosswalks) + " crosswalks found, " + str(remaing_time) + " seconds remaining"
            self._out(msg)


    def _calc_remaining_duration(self, percentage):
        to_do_percentage = 100 - percentage
        time_used = (datetime.datetime.now() - self.start_time).seconds
        time_remain = (time_used / percentage) * to_do_percentage
        return int(time_remain)


    def _out(self,msg, show_time=False):
        if self.verbose:
            output = msg
            if show_time:
                output = str(datetime.datetime.now()) + ": " + output
                print ""
            print output