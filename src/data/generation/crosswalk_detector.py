import os

from src.detection.deep.Convnet import Convnet


class CrosswalkDetector:
    def __init__(self, hdf5_file=None):
        self._TRESHOLD = 0.01  # The current convnet is very bad outside of zuerich, so I changed the threshold
        self.hdf5_file = hdf5_file
        self.convnet = Convnet()
        self._initialize()

    def detect(self, images):
        predictions = self.convnet.predict_crosswalks(images)
        detected_crosswalks = []
        for i in range(len(predictions)):
            if predictions[i]:
                detected_crosswalks.append(images[i])
        return detected_crosswalks

    def _initialize(self):
        self.convnet.threshold = self._TRESHOLD
        self.convnet.verbose = True
        if self.hdf5_file is not None:
            if not os.path.exists(self.hdf5_file):
                raise Exception('CSV file ' + self.hdf5_file + ' does not exist!')
            self.convnet.hdf5_file = self.hdf5_file
        self.convnet.initialize()
