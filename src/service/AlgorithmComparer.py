from src.base.Constants import Constants

class AlgorithmComparer:

    def __init__(self,detectedNodes, crosswalNodes):
        self.hits = 0
        for detectedNode in detectedNodes:
            for crosswalk in crosswalNodes:
                if detectedNode.getDistanceInMeter(crosswalk) <= Constants.RANGE_TO_NODE:
                    self.hits += 1
                    print 'Crosswalk: ' + str(crosswalk.toPoint()) + ' Detected: ' + str(detectedNode.toPoint())


        print 'detected: ' + str(len(detectedNodes))
        print 'crosswalks: ' + str(len(crosswalNodes))
        print 'hits: ' + str(self.hits)

    def getHits(self):
        return self.hits