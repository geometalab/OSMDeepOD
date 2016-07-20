from src.detection.deep.Convnet import Convnet


class CrosswalkDetector:
    def __init__(self, hdf5_file=None):
        self._TRESHOLD = 0.01  # The current convnet is very bad outside of zuerich, so I changed the threshold
        self.hdf5_file = hdf5_file

    def detect(self, images):
        convnet = Convnet()
        convnet.threshold = self._TRESHOLD
        convnet.verbose = True
        if self.hdf5_file is not None:
            convnet.hdf5_file = self.hdf5_file
        convnet.initialize()
        predictions = convnet.predict_crosswalks(images)
        detected_crosswalks = []
        for i in range(len(predictions)):
            if predictions[i]:
                detected_crosswalks.append(images[i])
        return detected_crosswalks
