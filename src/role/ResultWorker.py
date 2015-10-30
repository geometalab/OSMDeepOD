from rq import Queue, Connection, Worker
from src.base.Constants import Constants
from src.role.WorkerFunctions import store

class ResultWorker:
    def __init__(self):
        with Connection(Constants.REDIS):
            queues = [Constants.QUEUE_RESULTS]
            qs = map(Queue, queues) or [Queue()]
            w = Worker(qs)
            w.work()