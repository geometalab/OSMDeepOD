from src.role.WorkerFunctions import detect
from src.data.globalmaptiles import GlobalMercator
from src.base.Bbox import Bbox
from rq import Queue
from redis import Redis
import math


class Manager(object):
    SMALL_BBOX_SIDE_LENGHT = 2000.0
    TIMEOUT = 5400

    def __init__(self, bbox, jobqueue_name):
        self.big_bbox = bbox
        self.jobqueue_name = jobqueue_name
        self.mercator = GlobalMercator()
        self.small_bboxes = []

    @classmethod
    def from_big_bbox(cls, big_bbox, redis, jobqueue_name, apiKey):
        manager = cls(big_bbox, jobqueue_name)
        manager._generate_small_bboxes()
        manager._enqueue_jobs(redis, apiKey)
        return manager

    def _generate_small_bboxes(self):
        mminx, mminy = self.mercator.LatLonToMeters(
            self.big_bbox.bottom, self.big_bbox.left)
        rows = self._calc_rows()
        columns = self._calc_columns()
        side = Manager.SMALL_BBOX_SIDE_LENGHT

        for x in range(0, columns):
            for y in range(0, rows):
                bottom, left = self.mercator.MetersToLatLon(
                    mminx + (side * x),
                    mminy + (side * y))
                top, right = self.mercator.MetersToLatLon(
                    mminx + (side * (x + 1)),
                    mminy + (side * (y + 1)))
                small_bbox = Bbox.from_lbrt(left, bottom, right, top)
                self.small_bboxes.append(small_bbox)

    def _enqueue_jobs(self, redis, apiKey):
        redis_connection = Redis(redis[0], redis[1], password=redis[2])
        queue = Queue(self.jobqueue_name, connection=redis_connection)
        for small_bbox in self.small_bboxes:
            queue.enqueue_call(
                func=detect,
                args=(
                    small_bbox,
                    redis,
                    apiKey,
                ),
                timeout=Manager.TIMEOUT)

        print('Number of enqueued jobs in queue \'{0}\': {1}'.format(self.jobqueue_name, len(queue)))


    def _calc_rows(self):
        _, mminy = self.mercator.LatLonToMeters(
            self.big_bbox.bottom, self.big_bbox.left)
        _, mmaxy = self.mercator.LatLonToMeters(
            self.big_bbox.top, self.big_bbox.right)
        meter_in_y = mmaxy - mminy
        return int(math.ceil(meter_in_y / Manager.SMALL_BBOX_SIDE_LENGHT))

    def _calc_columns(self):
        mminx, _ = self.mercator.LatLonToMeters(
            self.big_bbox.bottom, self.big_bbox.left)
        mmaxx, _ = self.mercator.LatLonToMeters(
            self.big_bbox.top, self.big_bbox.right)
        meter_in_x = mmaxx - mminx
        return int(math.ceil(meter_in_x / Manager.SMALL_BBOX_SIDE_LENGHT))
