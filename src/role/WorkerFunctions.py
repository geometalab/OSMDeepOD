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
    with open('geo.json', 'r') as f:
        data = json.load(f)

    for x in range(0, len(nodes)):
        data.append(Point((nodes[x].longitude,nodes[x].latitude)))

    with open('geo.json', 'w') as f:
        json.dump(data, f)