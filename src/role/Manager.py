from src.role.WorkerFunctions import detect
from src.base.Constants import Constants
from src.data.globalmaptiles import GlobalMercator
from src.base.Bbox import Bbox
from rq import Queue
import math

class Manager:
    def __init__(self):
        self.big_bbox = Bbox()
        self.mercator = GlobalMercator()
        self.queue = Queue(Constants.QUEUE_JOBS, connection=Constants.REDIS)
        self.small_bboxes = []

    @classmethod
    def from_big_bbox(cls, big_bbox):
        manager = cls()
        manager.big_bbox = big_bbox
        manager._generate_small_bboxes()
        manager._enqueue_jobs()
        return manager

    def _generate_small_bboxes(self):
        mminx, mminy = self.mercator.LatLonToMeters(self.big_bbox.bottom, self.big_bbox.left)
        rows = self._calc_rows()
        columns = self._calc_columns()
        side = Constants.SMALL_BBOX_SIDE_LENGHT

        for x in range(0, columns):
            for y in range(0, rows):
                bottom, left = self.mercator.MetersToLatLon(mminx + (side * x), mminy + (side * y))
                top, right = self.mercator.MetersToLatLon(mminx + (side * (x + 1)), mminy + (side * (y + 1)))
                small_bbox = Bbox.from_lbrt(left, bottom, right, top)
                self.small_bboxes.append(small_bbox)
        self._enqueue_jobs()

    def _enqueue_jobs(self):
        for small_bbox in self.small_bboxes:
            self.queue.enqueue_call(func=detect, args=(small_bbox,), timeout=Constants.TIMEOUT)

    def _calc_rows(self):
        mminx, mminy = self.mercator.LatLonToMeters(self.big_bbox.bottom, self.big_bbox.left)
        mmaxx, mmaxy = self.mercator.LatLonToMeters(self.big_bbox.top, self.big_bbox.right)
        meter_in_y = mmaxy - mminy
        return int(math.ceil(meter_in_y / Constants.SMALL_BBOX_SIDE_LENGHT))

    def _calc_columns(self):
        mminx, mminy = self.mercator.LatLonToMeters(self.big_bbox.bottom, self.big_bbox.left)
        mmaxx, mmaxy = self.mercator.LatLonToMeters(self.big_bbox.top, self.big_bbox.right)
        meter_in_x = mmaxx - mminx
        return int(math.ceil(meter_in_x / Constants.SMALL_BBOX_SIDE_LENGHT))
