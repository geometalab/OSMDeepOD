import os
import environ
import numpy as np

import tensorflow as tf
from multiprocessing.pool import ThreadPool


class Detector:
    def __init__(self):
        self.graph_path = self._get_grap_paht()
        self.labels = ['noncrosswalk', 'crosswalk']
        self.graph_def = self._load_graph()

    def _get_grap_paht(self):
        directory = os.path.dirname(os.path.realpath(__file__))
        cwenv = environ.Env(GRAPH_PATH=(str, directory + '/output_graph_crosswalks.pb'))
        root = environ.Path(os.getcwd())
        environ.Env.read_env(root('.env'))
        return cwenv('GRAPH_PATH')

    def _load_graph(self):
        with tf.gfile.FastGFile(self.graph_path, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            return graph_def
            # _ = tf.import_graph_def(graph_def, name='')

    def detect(self, image):
        image_array = self._pil_to_tf(image)

        with tf.Graph().as_default() as imported_graph:
            tf.import_graph_def(self.graph_def, name='')

        with tf.Session(graph=imported_graph) as sess:
            with tf.device("/gpu:0"):
                softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
                predictions = sess.run(softmax_tensor, {'DecodeJpeg:0': image_array})
                predictions = np.squeeze(predictions)
                answer = {}
                for node_id in range(len(predictions)):
                    answer[self.labels[node_id]] = predictions[node_id]
                return answer

    def detect_multiple(self, images):
        image_array_list = [self._pil_to_tf(image) for image in images]

        pool = ThreadPool()
        with tf.Graph().as_default() as imported_graph:
            tf.import_graph_def(self.graph_def, name='')
            
        with tf.Session(graph=imported_graph) as sess:
            with tf.device("/gpu:0"):
                softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
                threads = [pool.apply_async(operation, args=(sess, softmax_tensor, image,)) for image in
                           image_array_list]
                results = []
                for x in threads:
                    results.append(x.get())

                return results

    @staticmethod
    def _pil_to_tf(image):
        return np.array(image)[:, :, 0:3]


def operation(sess, softmax, image):
    prediction = sess.run(softmax, {'DecodeJpeg:0': image})
    return prediction
