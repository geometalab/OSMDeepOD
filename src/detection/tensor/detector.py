import os
import environ
import numpy as np

import tensorflow as tf


class Detector:
    def __init__(self):
        self.graph_path = self._get_grap_paht()
        self.labels = ['noncrosswalk', 'crosswalk']
        self.sess = tf.Session()
        self._load_graph()

    def _get_grap_paht(self):
        cwenv = environ.Env(GRAPH_PATH=(str, 'graph_path'))
        root = environ.Path(os.getcwd())
        environ.Env.read_env(root('.env'))
        return cwenv('GRAPH_PATH')

    def _load_graph(self):
        with tf.device("/cpu:0"):
            with tf.gfile.FastGFile(self.graph_path, 'rb') as f:
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(f.read())
                _ = tf.import_graph_def(graph_def, name='')

    def _load_labels(self):
        with open(self.label_path, 'rb') as labels_file:
            lines = labels_file.readlines()
            return [w.decode("utf-8").replace("\n", "") for w in lines]

    def detect(self, image):
        image_array = self._pil_to_tf(image)
        with tf.device("/gpu:0"):
            softmax_tensor = self.sess.graph.get_tensor_by_name('final_result:0')
            predictions = self.sess.run(softmax_tensor, {'DecodeJpeg:0': image_array})
            predictions = np.squeeze(predictions)
            answer = {}
            for node_id in range(len(predictions)):
                answer[self.labels[node_id]] = predictions[node_id]
            return answer

    @staticmethod
    def _pil_to_tf(image):
        return np.array(image)[:, :, 0:3]
