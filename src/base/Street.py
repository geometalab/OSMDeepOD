class Street:

    def __init__(self):
        self.nodes = []
        self.name = ""
        self.ident = 0
        self.highway = "-"

    @classmethod
    def from_nodes(cls, node1, node2):
        street = cls()
        street.nodes.append(node1)
        street.nodes.append(node2)
        return street

    @classmethod
    def from_info(cls, name, ident, highway):
        street = cls()
        street.name = name
        street.ident = ident
        street.highway = highway
        return street

    def get_left_node(self):
        if self.nodes[0].longitude < self.nodes[1].longitude:
            return self.nodes[0]
        else:
            return self.nodes[1]

    def get_right_node(self):
        if self.nodes[0].longitude > self.nodes[1].longitude:
            return self.nodes[0]
        else:
            return self.nodes[1]
