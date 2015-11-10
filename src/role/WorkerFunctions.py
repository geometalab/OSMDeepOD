from src.base.Constants import Constants
from src.detection.BoxWalker import BoxWalker
from src.base.Crosswalk import Crosswalk
from rq import Queue
import json
import os

def detect(bbox):
    walker = BoxWalker(bbox)
    walker.loadTiles()
    walker.loadStreets()
    crosswalks = []
    crosswalkNodes = walker.walk()

    for node in crosswalkNodes:
        crosswalks.append(Crosswalk(node.latitude, node.longitude))

    q = Queue(Constants.QUEUE_RESULTS, connection=Constants.REDIS)
    q.enqueue(store, crosswalks)


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

