import rq
from rq import Queue
from rq import Connection
from redis import Redis


class Worker:

    def __init__(self):
        self.queues = []

    def run(self, redis):
        redis_connection = Redis(redis[0], redis[1], password=redis[2])
        with Connection(redis_connection):
            qs = map(Queue, self.queues) or [Queue()]
            w = rq.Worker(qs)
            w.work()

    @classmethod
    def from_worker(cls, queue):
        worker = cls()
        worker.queues = queue
        return worker
