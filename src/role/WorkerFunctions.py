from src.base.Constants import Constants
from rq import Queue
import json

def detect(bbox):
    #BoxWorker do work
    results = []
    q = Queue(Constants.QUEUE_RESULTS, connection=Constants.REDIS)
    q.enqueue(store, results)


def store(results):
    add_value = {'new_key': 'new_value'}
    with open('test.json') as f:
        data = json.load(f)

    data.update(add_value)

    with open('test.json', 'w') as f:
        json.dump(data, f)
