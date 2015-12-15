from src.base.Node import Node


class NodeMerger:
    def __init__(self):
        self.nodelist = None
        self.neardict = None
        self.max_distance = 7

    @classmethod
    def from_nodelist(cls, nodeList):
        merger = cls()
        merger.nodelist = nodeList
        return merger

    def _generate_neardict(self):
        nearDict = {}
        for me in self.nodelist:
            neighbors = []
            for other in self.nodelist:
                distance = me.get_distance_in_meter(other)
                if distance < self.max_distance and me != other:
                    neighbors.append(other)

            nearDict[me] = neighbors
        self.neardict = nearDict

    def reduce(self):
        mergedNodes = []
        self._generate_neardict()
        nodes = list(self.nodelist)

        while len(nodes) > 0:
            me = nodes[0]
            subGraph = self._get_neighbors(me)
            merged = self._merge(subGraph)
            mergedNodes.append(merged)
            for node in subGraph:
                if not node in nodes:
                    print ""
                nodes.remove(node)
        return  mergedNodes

    def _merge(self, subGraph):
        nodeCount = len(subGraph)
        latitudeSum = 0
        longitudeSum = 0
        for node  in subGraph:
            latitudeSum += node.latitude
            longitudeSum += node.longitude

        latitude = latitudeSum /nodeCount
        longitude = longitudeSum / nodeCount
        merged = Node(latitude, longitude, 0)
        return merged


    def _get_neighbors(self, node):
        ret = [node]
        ret += self._get_neighbors2(node,list(self.nodelist))
        return ret

    def _get_neighbors2(self, node, nodeNotYetConsiderd = []):
        if len(nodeNotYetConsiderd) == 0:
            return []
        nodeNotYetConsiderd.remove(node)
        ret = []
        for other in self.neardict[node]:
            if other in nodeNotYetConsiderd:
                ret.append(other)
                ret += self._get_neighbors2(other,nodeNotYetConsiderd)
        return ret