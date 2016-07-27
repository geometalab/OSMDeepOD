import math
from rq import Queue
from redis import Redis

from .worker_functions import detect
from ..data.globalmaptiles import GlobalMercator
from ..base.bbox import Bbox


class Manager(object):
    SMALL_BBOX_SIDE_LENGHT = 2000.0
    TIMEOUT = 5400

    def __init__(self, bbox, job_queue_name):
        self.big_bbox = bbox
        self.job_queue_name = job_queue_name
        self.mercator = GlobalMercator()
        self.small_bboxes = []

    @classmethod
    def from_big_bbox(cls, big_bbox, redis, job_queue_name, apiKey):
        manager = cls(big_bbox, job_queue_name)
        manager._generate_small_bboxes()
        manager._enqueue_jobs(redis, apiKey)
        return manager

    def _generate_small_bboxes(self):
        m_minx, m_miny = self.mercator.LatLonToMeters(self.big_bbox.bottom, self.big_bbox.left)
        rows = self._calc_rows()
        columns = self._calc_columns()
        side = Manager.SMALL_BBOX_SIDE_LENGHT

        for x in range(0, columns):
            for y in range(0, rows):
                bottom, left = self.mercator.MetersToLatLon(m_minx + (side * x), m_miny + (side * y))
                top, right = self.mercator.MetersToLatLon(m_minx + (side * (x + 1)), m_miny + (side * (y + 1)))
                small_bbox = Bbox.from_lbrt(left, bottom, right, top)
                self.small_bboxes.append(small_bbox)

    def _enqueue_jobs(self, redis, api_key):
        redis_connection = Redis(redis[0], redis[1], password=redis[2])
        queue = Queue(self.job_queue_name, connection=redis_connection)
        for small_bbox in self.small_bboxes:
            queue.enqueue_call(
                    func=detect,
                    args=(small_bbox, redis, api_key,),
                    timeout=Manager.TIMEOUT)
        print('Number of enqueued jobs in queue \'{0}\': {1}'.format(self.job_queue_name, len(queue)))

    def _calc_rows(self):
        _, m_miny = self.mercator.LatLonToMeters(self.big_bbox.bottom, self.big_bbox.left)
        _, m_maxy = self.mercator.LatLonToMeters(self.big_bbox.top, self.big_bbox.right)
        meter_in_y = m_maxy - m_miny
        return int(math.ceil(meter_in_y / Manager.SMALL_BBOX_SIDE_LENGHT))

    def _calc_columns(self):
        m_minx, _ = self.mercator.LatLonToMeters(self.big_bbox.bottom, self.big_bbox.left)
        m_maxx, _ = self.mercator.LatLonToMeters(self.big_bbox.top, self.big_bbox.right)
        meter_in_x = m_maxx - m_minx
        return int(math.ceil(meter_in_x / Manager.SMALL_BBOX_SIDE_LENGHT))
