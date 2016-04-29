from __future__ import absolute_import
from __future__ import print_function

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.regularizers import l2
import theano
import os
import numpy as np


class Convnet(object):

    def __init__(self):
        self.verbose = True
        self.very_verbose = False
        self.model = None
        self.hdf5_file = "convnet48.e158-l0.055.hdf5"
        self.threshold = 0.9

    @classmethod
    def from_verbose(cls, verbose=True):
        convnet = cls()
        convnet.verbose = verbose
        return convnet

    def _out(self, msg):
        if self.verbose:
            print(msg)

    def initialize(self):
        self._enable_multithreading()
        self._out("Compile convnet")
        self.model = self._compile_model()
        self._out("Load " + self.hdf5_file)
        self._load_weights(self.hdf5_file)

    def is_initialized(self):
        return not self.model is None

    def predict_crosswalks(self, pil_image_list):
        numpy_arr = self._to_numpy_array(pil_image_list)
        x = self._normalize(numpy_arr)
        results = self._predict_list(x)
        return results

    def _to_numpy_array(self, pil_image_list):
        x = np.zeros((len(pil_image_list), 50, 50, 3))
        for idx, val in enumerate(pil_image_list):
            img = np.array(val)
            x[idx] = img
        return x

    def _normalize(self, numpy_array):
        x = numpy_array.reshape(numpy_array.shape[0], 3, 50, 50)
        x = x.astype("float32")
        x /= 255
        return x

    def _predict_list(self, x):
        predictions = self.model.predict(x)
        results = []
        for predict in predictions:
            isCrosswalk = predict[0] > self.threshold

            if self.very_verbose:
                if isCrosswalk:
                    print ("Zebra: " + str(predict))
                else:
                    print(str(predict))

            results.append(isCrosswalk)
        return results

    def _enable_multithreading(self):
        theano.config.openmp = True

    def _compile_model(self):
        # input image dimensions
        img_rows, img_cols = 50, 50
        # number of convolutional filters to use
        nb_filters1 = 48
        nb_filters2 = 128
        nb_filters3 = 256
        # size of pooling area for max pooling
        nb_pool = 2
        # convolution kernel size
        nb_conv = 3
        #image is rgb
        img_channels = 3

        # Lamda for L2 regularization
        lmda_dense = 8e-5
        lmda_conv = 8e-5

        model = Sequential()

        model.add(
            Convolution2D(
                nb_filters1,
                nb_conv,
                nb_conv,
                W_regularizer=l2(lmda_conv),
                border_mode='same',
                input_shape=(
                    img_channels,
                    img_rows,
                    img_cols)))
        model.add(Activation('relu'))
        model.add(Dropout(0.2))
        model.add(
            Convolution2D(
                nb_filters1,
                nb_conv,
                nb_conv,
                W_regularizer=l2(lmda_conv)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))

        model.add(Dropout(0.5))
        model.add(
            Convolution2D(
                nb_filters2,
                nb_conv,
                nb_conv,
                W_regularizer=l2(lmda_conv)))
        model.add(Activation('relu'))
        model.add(Dropout(0.2))
        model.add(
            Convolution2D(
                nb_filters2,
                nb_conv,
                nb_conv,
                W_regularizer=l2(lmda_conv)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))

        model.add(Dropout(0.5))
        model.add(
            Convolution2D(
                nb_filters3,
                nb_conv,
                nb_conv,
                W_regularizer=l2(lmda_conv)))
        model.add(Activation('relu'))
        model.add(Dropout(0.2))
        model.add(
            Convolution2D(
                nb_filters3,
                nb_conv,
                nb_conv,
                W_regularizer=l2(lmda_conv)))
        model.add(Activation('relu'))
        model.add(Dropout(0.2))
        model.add(Convolution2D(nb_filters3, nb_conv, nb_conv))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))

        model.add(Flatten())

        model.add(Dropout(0.5))
        model.add(Dense(2048, W_regularizer=l2(lmda_dense)))
        model.add(Activation('relu'))

        model.add(Dropout(0.5))
        model.add(Dense(1024, W_regularizer=l2(lmda_dense)))
        model.add(Activation('relu'))

        model.add(Dropout(0.5))
        model.add(Dense(2, W_regularizer=l2(lmda_dense)))
        model.add(Activation('softmax'))

        model.compile(loss='categorical_crossentropy', optimizer='adadelta')
        return model

    def _load_weights(self, hdf5_file):
        current_dir = os.path.join(os.getcwd(), os.path.dirname(__file__))

        network_path = ""
        if self._is_docker_container():
            # Docker makes some crucial tricks in the filesystem
            # virtualization. If it's a docker then we use this path
            network_path = '/root/OSM-Crosswalk-Detection/src/detection/deep/' + hdf5_file
        else:
            network_path = current_dir + "/" + hdf5_file

        self.model.load_weights(network_path)

    def _is_docker_container(self):
        return os.path.exists('/root/OSM-Crosswalk-Detection/DockerIam')
