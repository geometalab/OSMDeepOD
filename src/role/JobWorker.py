from rq import Queue, Connection, Worker
from src.base.Constants import Constants
from src.role.WorkerFunctions import detect

class JobWorker:
    def __init__(self):
        with Connection(Constants.REDIS):
            queues = [Constants.QUEUE_JOBS, Constants.QUEUE_FAILED]
            qs = map(Queue, queues) or [Queue()]
            w = Worker(qs)
            w.work()