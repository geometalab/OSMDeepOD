class Street(object):
    def __init__(self, nodes=None):
        self.nodes = [] if nodes is None else nodes
