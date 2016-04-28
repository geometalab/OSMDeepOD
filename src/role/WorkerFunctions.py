from src.detection.BoxWalker import BoxWalker
from rq import Queue
from redis import Redis
import json
import os
from src import cwenv


def detect(bbox, redis):
    walker = BoxWalker(bbox)
    walker.load_convnet()
    walker.load_tiles()
    walker.load_streets()
    crosswalkNodes = walker.walk()
    redis_connection = Redis(redis[0], redis[1], password=redis[2])
    q = Queue('results', connection=redis_connection)
    q.enqueue_call(func=store, args=(crosswalkNodes,), timeout=5400)

PATH_TO_CROSSWALKS = os.path.join(
    cwenv(
        'OUTPUT_DIR',
        default='.'),
    'crosswalks.json')


def store(crosswalks):
    if not os.path.exists(PATH_TO_CROSSWALKS):
        with open(PATH_TO_CROSSWALKS, 'w') as f:
            f.write('{ "crosswalks" : []}')

    with open(PATH_TO_CROSSWALKS, 'r') as f:
        data = json.load(f)

    for crosswalk in crosswalks:
        data['crosswalks'].append(
            {"latitude": crosswalk.latitude, "longitude": crosswalk.longitude})

    with open(PATH_TO_CROSSWALKS, 'w') as f:
        json.dump(data, f)
