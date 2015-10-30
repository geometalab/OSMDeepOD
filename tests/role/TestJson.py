import unittest
import json
from src.base.Node import Node
from geojson import Point

class TestJson(unittest.TestCase):

    def test(self):
        nodes = []
        node1 = Node(47.123638, 9.303093, 100)
        node2 = Node(47.123633, 9.303090, 101)
        nodes.append(node1)
        nodes.append(node2)
        with open('geo.json', 'r') as f:
            data = json.load(f)

        print Point((node1.longitude, node1.latitude))

        print dir(data)
        for x in range(0, len(nodes)):
            print nodes[x].longitude
            print nodes[x].latitude
            data.append(Point((nodes[x].longitude,nodes[x].latitude)))

        with open('geo.json', 'w') as f:
            json.dump(data, f)
