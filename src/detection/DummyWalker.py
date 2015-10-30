from src.base.Node import Node

class DummyWalker:
    def __init__(self):
        pass

    def detect(self, bbox):
        nodes = []
        node1 = Node(47.123638, 9.303093, 100)
        node2 = Node(47.123633, 9.303090, 101)
        nodes.append(node1)
        nodes.append(node2)
        return nodes