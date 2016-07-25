import warnings
import numpy as np
import os

import tensorflow as tf


class Detector:
    def __init__(self, graph_path='output_graph_crosswalks.pb', label_path='output_labels_crosswalks.txt'):
        current_dir = os.path.dirname(__file__)
        self.graph_path = current_dir + '/' + graph_path
        self.label_path = current_dir + '/' + label_path
        self.labels = self._load_labels()
        self.sess = tf.Session()
        self._load_graph()

    def __del__(self):
        self.sess.close()

    def _load_graph(self):
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
