from src.data.node_loader import NodeLoader


class OsmComparer:
    def __init__(self, max_distance=7):
        self.max_distance = max_distance

    def compare(self, detected_nodes, bbox, tag):
        osm_nodes = self._load_nodes(bbox, tag)
        return self._compare_osm_with(osm_nodes, detected_nodes)

    def _load_nodes(self, bbox, tag):
        node_loader = NodeLoader()
        return node_loader.load_data(bbox, tag)

    def _compare_osm_with(self, osm_nodes, detected_nodes):
        compared_nodes = []
        is_near = False
        for detected_node in detected_nodes:
            for node in osm_nodes:
                if node.get_distance_in_meter(detected_node) < self.max_distance:
                    is_near = True
                    break
            if not is_near:
                compared_nodes.append(detected_node)
            is_near = False
        return compared_nodes
