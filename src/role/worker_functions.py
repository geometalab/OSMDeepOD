from rq import Queue
from redis import Redis
import json
import os

from src import cwenv
from src.detection.box_walker import BoxWalker


def detect(bbox, redis, zoom_level):
    walker = BoxWalker(bbox=bbox, zoom_level=zoom_level)
    walker.load_streets()
    crosswalk_nodes = []
    if len(walker.streets) > 0:
        walker.load_convnet()
        walker.load_tiles()
        crosswalk_nodes = walker.walk()
    redis_connection = Redis(redis[0], redis[1], password=redis[2])
    q = Queue('results', connection=redis_connection)
    q.enqueue_call(func=store, args=(crosswalk_nodes,), timeout=5400)


PATH_TO_CROSSWALKS = os.path.join(cwenv('OUTPUT_DIR', default='.'), 'crosswalks.json')


def store(crosswalks):
    if not os.path.exists(PATH_TO_CROSSWALKS):
        with open(PATH_TO_CROSSWALKS, 'w') as f:
            f.write('{ "crosswalks" : []}')

    with open(PATH_TO_CROSSWALKS, 'r') as f:
        data = json.load(f)

    for crosswalk in crosswalks:
        data['crosswalks'].append({"latitude": crosswalk.latitude, "longitude": crosswalk.longitude})

    with open(PATH_TO_CROSSWALKS, 'w') as f:
        json.dump(data, f)

    print('{0} potential crosswalks detected so far'.format(len(data['crosswalks'])))
