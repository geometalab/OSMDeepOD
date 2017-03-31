from rq import Queue
from redis import Redis
import json
import os

from src.detection.box_walker import BoxWalker


def enqueue_results(result_nodes, redis_connection):
    q = Queue('results', connection=redis_connection)
    q.enqueue_call(func=store, args=(result_nodes,), timeout=5400)
    for result_node in result_nodes:
        redis_connection.rpush('visualizing', result_node.to_geojson())


def get_nodes(bbox, configuration):
    walker = BoxWalker(bbox=bbox, configuration=configuration)
    if configuration.DETECTION.followstreets:
        walker.load_streets()
    crosswalk_nodes = []
    if len(walker.streets) > 0 or not configuration.follow_streets:
        walker.load_convnet()
        walker.load_tiles()
        crosswalk_nodes = walker.walk()
    return crosswalk_nodes


def detect(bbox, configuration):
    nodes = get_nodes(bbox, configuration)
    redis_connection = Redis(host=configuration.server, port=configuration.port, password=configuration.password)
    enqueue_results(nodes, redis_connection)


def store(nodes):
    store_path = os.path.join(os.getcwd(), 'detected_nodes.json')
    if not os.path.exists(store_path):
        with open(store_path, 'w') as f:
            f.write('{ "nodes" : []}')

    with open(store_path, 'r') as f:
        data = json.load(f)

    for node in nodes:
        data['nodes'].append({"latitude": node.latitude, "longitude": node.longitude})

    with open(store_path, 'w') as f:
        json.dump(data, f)

    print('{0} potential nodes detected so far'.format(len(data['nodes'])))


def standalone(bboxes=None, configuration=None):
    nodes = []
    for bbox in bboxes:
        nodes += get_nodes(bbox, configuration)
    store(nodes)
