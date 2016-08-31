import math

from redis import Redis
from rq import Queue

from src.base.bbox import Bbox
from src.base.search import Search
from src.base.globalmaptiles import GlobalMercator
from src.role.worker_functions import detect


class Manager(object):
    small_bbox_side_length = 2000.0
    timeout = 5400

    def __init__(self, bbox, job_queue_name, zoom_level=19, search=Search()):
        self.big_bbox = bbox
        self.job_queue_name = job_queue_name
        self.mercator = GlobalMercator()
        self.small_bboxes = []
        self.zoom_level = zoom_level
        self.search = search

    @classmethod
    def from_big_bbox(cls, big_bbox, redis, job_queue_name, zoom_level=19, search='crosswalk'):
        manager = cls(big_bbox, job_queue_name, zoom_level, search)
        manager._generate_small_bboxes()
        manager._enqueue_jobs(redis)
        return manager

    def _generate_small_bboxes(self):
        m_minx, m_miny = self.mercator.LatLonToMeters(self.big_bbox.bottom, self.big_bbox.left)
        rows = self._calc_rows()
        columns = self._calc_columns()
        side = Manager.small_bbox_side_length

        for x in range(0, columns):
            for y in range(0, rows):
                bottom, left = self.mercator.MetersToLatLon(m_minx + (side * x), m_miny + (side * y))
                top, right = self.mercator.MetersToLatLon(m_minx + (side * (x + 1)), m_miny + (side * (y + 1)))
                small_bbox = Bbox.from_lbrt(left, bottom, right, top)
                self.small_bboxes.append(small_bbox)

    def _enqueue_jobs(self, redis):
        redis_connection = Redis(redis[0], redis[1], password=redis[2])
        queue = Queue(self.job_queue_name, connection=redis_connection)
        for small_bbox in self.small_bboxes:
            queue.enqueue_call(
                func=detect,
                args=(small_bbox, redis, self.zoom_level, self.search),
                timeout=Manager.timeout)
        print('Number of enqueued jobs in queue \'{0}\': {1}'.format(self.job_queue_name, len(queue)))

    def _calc_rows(self):
        _, m_miny = self.mercator.LatLonToMeters(self.big_bbox.bottom, self.big_bbox.left)
        _, m_maxy = self.mercator.LatLonToMeters(self.big_bbox.top, self.big_bbox.right)
        meter_in_y = m_maxy - m_miny
        return int(math.ceil(meter_in_y / Manager.small_bbox_side_length))

    def _calc_columns(self):
        m_min_x, _ = self.mercator.LatLonToMeters(self.big_bbox.bottom, self.big_bbox.left)
        m_max_x, _ = self.mercator.LatLonToMeters(self.big_bbox.top, self.big_bbox.right)
        meter_in_x = m_max_x - m_min_x
        return int(math.ceil(meter_in_x / Manager.small_bbox_side_length))
