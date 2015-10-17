from src.base.Node import Node


class NodeMerger:
    def __init__(self):
        self.nodeList = None
        self.nearDict = None
        self.maxDistance = 7

    @classmethod
    def fromNodeList(cls, nodeList):
        merger = cls()
        merger.nodeList = nodeList
        return merger

    def generateNearDict(self):
        nearDict = {}
        for me in self.nodeList:
            neighbors = []
            for other in self.nodeList:
                distance = me.getDistanceInMeter(other)
                if(distance < self.maxDistance and me != other):
                    neighbors.append(other)

            nearDict[me] = neighbors
        self.nearDict = nearDict

    def isNeighbor(self, n1, n2):
        list = self.nodeList[n1]
        return n2 in list

    def reduce(self):
        mergedNodes = []
        self.generateNearDict()
        nodes = list(self.nodeList)

        while(len(nodes) > 0):
            me = nodes[0]
            subGraph = self.getNeighbors(me)
            merged = self.merge(subGraph)
            mergedNodes.append(merged)
            for node in subGraph:
                if(not node in nodes):
                    print ""
                nodes.remove(node)
        return  mergedNodes

    def merge(self, subGraph):
        nodeCount = len(subGraph)
        latitudeSum = 0
        longitudeSum = 0
        for node  in subGraph:
            latitudeSum += node.lat
            longitudeSum += node.lon

        latitude = latitudeSum /nodeCount
        longitude = longitudeSum / nodeCount
        merged = Node(0, latitude, longitude)
        return merged


    def getNeighbors(self, node):
        ret = [node]
        ret += self.__getNeighbors(node,list(self.nodeList))
        return ret

    def __getNeighbors(self, node, nodeNotYetConsiderd = []):
        if(len(nodeNotYetConsiderd) == 0):
            return []
        nodeNotYetConsiderd.remove(node)
        ret = []
        for other in self.nearDict[node]:
            if(other in nodeNotYetConsiderd):
                ret.append(other)
                ret += self.__getNeighbors(other,nodeNotYetConsiderd)
        return ret







    def removeNodeInDict(self, node):
        self.nearDict[node] = []
        for other in self.nodeList:
            list = self.nearDict[other]
            list.remove(other)
            self.nearDict[other] = list



