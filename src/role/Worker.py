import rq
from rq import Queue
from rq import Connection
from redis import Redis


class Worker(object):

    def __init__(self, jobqueue_name_list):
        self.queues = jobqueue_name_list

    def run(self, redis):
        redis_connection = Redis(redis[0], redis[1], password=redis[2])
        with Connection(redis_connection):
            qs = map(Queue, self.queues) or [Queue()]
            w = rq.Worker(qs)
            w.work()
            try:
                print('Items in queue \'{0}\': {1}'.format(self.queues[0], len(qs)))
            except:
                pass

    @classmethod
    def from_worker(cls, jobqueue_name_list):
        return cls(jobqueue_name_list)
