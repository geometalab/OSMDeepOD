from src.base.Constants import Constants
from src.detection.BoxWalker import BoxWalker
from rq import Queue
import json
import os

def detect(bbox):
    walker = BoxWalker(bbox)
    walker.load_convnet()
    walker.loadTiles()
    walker.loadStreets()
    crosswalkNodes = walker.walk()



    q = Queue(Constants.QUEUE_RESULTS, connection=Constants.REDIS)
    q.enqueue_call(func=store, args=(crosswalkNodes,), timeout=Constants.TIMEOUT)

def store(crosswalks):
    if not os.path.exists(Constants.PATH_TO_CROSSWALKS):
        with open(Constants.PATH_TO_CROSSWALKS, 'w') as f:
            f.write('{ "crosswalks" : []}')

    with open(Constants.PATH_TO_CROSSWALKS, 'r') as f:
        data = json.load(f)

    for crosswalk in crosswalks:
        data['crosswalks'].append({"latitude":crosswalk.latitude, "longitude":crosswalk.longitude})

    with open(Constants.PATH_TO_CROSSWALKS, 'w') as f:
        json.dump(data, f)

