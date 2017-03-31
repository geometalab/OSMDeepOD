import math

from redis import Redis
from rq import Queue

from src.base.bbox import Bbox
from src.base.configuration import Configuration
from src.base.globalmaptiles import GlobalMercator
from src.role import worker_functions


class Manager:
    def __init__(self, bbox=None, configuration=None, standalone=False):
        self.standalone = standalone
        self.big_bbox = bbox
        self.job_queue_name = 'jobs'
        self.mercator = GlobalMercator()
        self.small_bboxes = []
        self.configuration = configuration

    def run(self):
        self._generate_small_bboxes()
        if not self.standalone:
            self._enqueue_jobs(self.configuration)
        else:
            worker_functions.standalone(bboxes=self.small_bboxes, configuration=self.configuration)

    def _generate_small_bboxes(self):
        m_minx, m_miny = self.mercator.LatLonToMeters(self.big_bbox.bottom, self.big_bbox.left)
        rows = self._calc_rows()
        columns = self._calc_columns()
        side = int(self.configuration.JOB.bboxsize)

        for x in range(0, columns):
            for y in range(0, rows):
                bottom, left = self.mercator.MetersToLatLon(m_minx + (side * x), m_miny + (side * y))
                top, right = self.mercator.MetersToLatLon(m_minx + (side * (x + 1)), m_miny + (side * (y + 1)))
                small_bbox = Bbox(left=left, bottom=bottom, right=right, top=top)
                self.small_bboxes.append(small_bbox)

    def _enqueue_jobs(self, configuration):
        redis_connection = Redis(host=configuration.server, port=configuration.port, password=configuration.password)
        queue = Queue(self.job_queue_name, connection=redis_connection)
        for small_bbox in self.small_bboxes:
            queue.enqueue_call(func=worker_functions.detect, args=(small_bbox, self.configuration),
                               timeout=self.configuration.timeout)
        print('Number of enqueued jobs in queue \'{0}\': {1}'.format(self.job_queue_name, len(queue)))

    def _calc_rows(self):
        _, m_miny = self.mercator.LatLonToMeters(self.big_bbox.bottom, self.big_bbox.left)
        _, m_maxy = self.mercator.LatLonToMeters(self.big_bbox.top, self.big_bbox.right)
        meter_in_y = m_maxy - m_miny
        return int(math.ceil(meter_in_y / int(self.configuration.JOB.bboxsize)))

    def _calc_columns(self):
        m_min_x, _ = self.mercator.LatLonToMeters(self.big_bbox.bottom, self.big_bbox.left)
        m_max_x, _ = self.mercator.LatLonToMeters(self.big_bbox.top, self.big_bbox.right)
        meter_in_x = m_max_x - m_min_x
        return int(math.ceil(meter_in_x / int(self.configuration.JOB.bboxsize)))
