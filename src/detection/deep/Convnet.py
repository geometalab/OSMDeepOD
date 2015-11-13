from __future__ import absolute_import
from __future__ import print_function

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.regularizers import l2
import theano
import os
import numpy as np



def _load_64f4c(hd5f_path, verbose):

    batch_size = 128
    nb_classes = 2
    nb_epoch = 12

    # input image dimensions
    img_rows, img_cols = 50, 50
    # number of convolutional filters to use
    nb_filters = 64
    # size of pooling area for max pooling
    nb_pool = 2
    # convolution kernel size
    nb_conv = 4#3
    #image is rgb
    img_channels = 3


    if(verbose):
        print("put convnet together")
    model = Sequential()

    model.add(Convolution2D(nb_filters, nb_conv, nb_conv, border_mode='full', input_shape=(img_channels, img_rows, img_cols)))
    model.add(Activation('relu'))
    model.add(Convolution2D(nb_filters, nb_conv, nb_conv))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    if(verbose):
        print("start compiling")
    model.compile(loss='categorical_crossentropy', optimizer='adadelta')
    if(verbose):
        print("load weights")
    model.load_weights(hd5f_path)
    if(verbose):
        print("network loaded")

    return model

def predictCrosswalks(pilimg_list):
    x = np.zeros((len(pilimg_list), 50, 50, 3))
    for i in range(len(pilimg_list)):
        img = np.array(pilimg_list[i])
        x[i] = img
    x = x.reshape(x.shape[0], 3, 50, 50)

    results = _predict_list(x)
    return results

def _predict_list(x):
    global last_prediction
    predictions = network.predict(x)
    results = []
    for predict in predictions:
        isCrosswalk = predict[0] > 0.999 and predict[1] < 1e-300
        if(isCrosswalk): print("Zerba " + str(predict))
        #else: print(str(predict))
        results.append(isCrosswalk)
    last_prediction = predictions
    return results

network = None
last_prediction = None

def initialize():
    global network
    _enable_keras_multithreading()
    current_dir = os.path.join(os.getcwd(), os.path.dirname(__file__))
    #Best Net 64f4:

    network_path = current_dir + "/" + "klein64-4f.e11-l0.045.hdf5"
    network = _load_64f4c(network_path, True)
    #Schwellwert: 1e-150, isCrosswalk = predict[0] > 0.9 and predict[1] < 1e-150

def _enable_keras_multithreading():
    theano.config.openmp = True
