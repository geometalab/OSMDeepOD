from src.base.node import Node


class NodeMerger:
    def __init__(self, node_list=None, max_distance=8):
        self.node_list = [] if node_list is None else node_list
        self.near_dict = {}
        self.max_distance = max_distance

    @classmethod
    def from_nodelist(cls, node_list):
        merger = cls()
        merger.node_list = node_list
        return merger

    def _generate_near_dict(self):
        near_dict = {}
        for me in self.node_list:
            neighbors = []
            for other in self.node_list:
                distance = me.get_distance_in_meter(other)
                if distance < self.max_distance and me != other:
                    neighbors.append(other)
            near_dict[me] = neighbors
        self.near_dict = near_dict

    def reduce(self):
        merged_nodes = []
        self._generate_near_dict()
        nodes = list(self.node_list)

        while len(nodes) > 0:
            me = nodes[0]
            sub_graph = self._get_neighbors(me)
            merged = self._merge(sub_graph)
            merged_nodes.append(merged)
            for node in sub_graph:
                if node in nodes:
                    nodes.remove(node)
        return list(set(merged_nodes))

    @staticmethod
    def _merge(sub_graph):
        node_count = len(sub_graph)
        latitude_sum = 0
        longitude_sum = 0
        for node in sub_graph:
            latitude_sum += node.latitude
            longitude_sum += node.longitude

        latitude = latitude_sum / node_count
        longitude = longitude_sum / node_count
        merged = Node(latitude, longitude, 0)
        return merged

    def _get_neighbors(self, node):
        ret = [node]
        ret += self._get_neighbors2(node, list(self.node_list))
        return ret

    def _get_neighbors2(self, node, node_not_yet_considered):
        if len(node_not_yet_considered) == 0:
            return []
        node_not_yet_considered.remove(node)
        ret = []
        for other in self.near_dict[node]:
            if other in node_not_yet_considered:
                ret.append(other)
                ret += self._get_neighbors2(other, node_not_yet_considered)
        return ret
