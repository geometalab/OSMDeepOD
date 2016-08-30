import os
import environ
import numpy as np

import tensorflow as tf
from multiprocessing.pool import ThreadPool


class Detector:
    def __init__(self, graph_file='output_graph.pb', labels_file='output_labels.txt'):
        self.current_directory = os.path.dirname(os.path.realpath(__file__))
        self.graph_file = graph_file
        self.labels_file = labels_file
        self.env = self._get_env()
        self.labels = self._load_labels()
        self.graph_def = self._load_graph()

    def _get_env(self):
        env = environ.Env(GRAPH_PATH=(str, self.current_directory + '/' + self.graph_file),
                          LABEL_PATH=(str, self.current_directory + '/' + self.labels_file))
        root = environ.Path(os.getcwd())
        environ.Env.read_env(root('.env'))
        return env

    def _load_labels(self):
        return [line.rstrip('\n') for line in open(self.env('LABEL_PATH'))]

    def _load_graph(self):
        with tf.gfile.FastGFile(self.env('GRAPH_PATH'), 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            return graph_def

    def detect(self, images):
        np_images = [self._pil_to_np(image) for image in images]

        pool = ThreadPool()
        with tf.Graph().as_default() as imported_graph:
            tf.import_graph_def(self.graph_def, name='')

        with tf.Session(graph=imported_graph) as sess:
            with tf.device("/gpu:0"):
                softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
                threads = [pool.apply_async(self.operation,
                                            args=(sess, softmax_tensor, np_images[image_number], image_number,)) for
                           image_number in range(len(np_images))]
                answers = []
                for thread in threads:
                    prediction, image_number = thread.get()
                    prediction = np.squeeze(prediction)
                    answer = {'image_number': image_number}
                    for node_id, _ in enumerate(prediction):
                        answer[self.labels[node_id]] = prediction[node_id]
                    answers.append(answer)
                return answers

    @staticmethod
    def _pil_to_np(image):
        return np.array(image)[:, :, 0:3]

    @staticmethod
    def operation(sess, softmax, image, image_number):
        prediction = sess.run(softmax, {'DecodeJpeg:0': image})
        return prediction, image_number
