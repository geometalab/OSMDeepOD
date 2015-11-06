from rq import Worker
from rq import Queue
from rq import Connection
from src.base.Constants import Constants
from src.role.WorkerFunctions import detect
from src.role.WorkerFunctions import store

class Worker:
    def __init__(self):
        self.queues = None

    def run(self):
        with Connection(Constants.REDIS):
            qs = map(Queue, self.queues) or [Queue()]
            w = Worker(qs)
            w.work()

    @classmethod
    def from_worker(cls, queues=[Constants.QUEUE_JOBS]):
        worker = cls()
        worker.queues = queues
        return worker
