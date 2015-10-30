from src.base.Constants import Constants
from rq import Queue
from src.detection.DummyWalker import DummyWalker
import json
from geojson import Point

def detect(bbox):
    walker = DummyWalker()
    nodes = walker.detect(bbox)
    q = Queue(Constants.QUEUE_RESULTS, connection=Constants.REDIS)
    q.enqueue(store, nodes)


def store(nodes):
    for x in range(0, len(nodes)):
        print str(nodes[x].longitude) + '  ' +  str(nodes[x].latitude)
