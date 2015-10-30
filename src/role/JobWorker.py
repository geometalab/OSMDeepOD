from rq import Worker
from rq import Queue
from rq import Connection
from src.base.Constants import Constants
from src.role.WorkerFunctions import detect

class JobWorker:
    def __init__(self):
        pass

    def run(self):
        print 'I start to work!'
        with Connection(Constants.REDIS):
            print 'Connected!'
            queues = [Constants.QUEUE_JOBS, Constants.QUEUE_FAILED]
            qs = map(Queue, queues) or [Queue()]
            w = Worker(qs)
            w.work()

