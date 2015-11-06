from src.base.Constants import Constants
from rq import Queue
import json
import os

def detect(bbox):
    pass
    #walker = DummyWalker()
    #nodes = walker.detect(bbox)
    #q = Queue(Constants.QUEUE_RESULTS, connection=Constants.REDIS)
    #q.enqueue(store, nodes)


def store(crosswalks):
    if not os.path.exists(Constants.PATH_TO_CROSSWALKS):
        with open(Constants.PATH_TO_CROSSWALKS, 'w') as f:
            f.write('{ "crosswalks" : []}')

    with open(Constants.PATH_TO_CROSSWALKS, 'r') as f:
        data = json.load(f)

    for crosswalk in crosswalks:
        data['crosswalks'].append({"latitude":crosswalk.latitude, "longitude":crosswalk.longitude, "osm_street_id":crosswalk.osm_street_id})

    with open(Constants.PATH_TO_CROSSWALKS, 'w') as f:
        json.dump(data, f)

