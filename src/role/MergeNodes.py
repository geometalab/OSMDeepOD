import os
import json
from src.base.Node import Node
from src.detection.NodeMerger import NodeMerger

input_file = 'crosswalks.json'

if not os.path.exists(input_file):
    exit()

with open(input_file, 'r') as f:
        data = json.load(f)

nodes = []
for crosswalk in data['crosswalks']:
    node = Node(crosswalk['latitude'], crosswalk['longitude'])
    nodes.append(node)

nodeMerger = NodeMerger().from_nodelist(nodes)
mergedNodes = nodeMerger.reduce()

new_file = 'new_crosswalks.json'

if not os.path.exists(new_file):
    with open(new_file, 'w') as f:
        f.write('{ "crosswalks" : []}')

    with open(new_file, 'r') as f:
        data = json.load(f)

    for crosswalk in mergedNodes:
        data['crosswalks'].append({"latitude":crosswalk.latitude, "longitude":crosswalk.longitude})

    with open(new_file, 'w') as f:
        json.dump(data, f)
