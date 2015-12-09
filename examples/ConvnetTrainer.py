from __future__ import absolute_import
from __future__ import print_function

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.regularizers import l2
from keras import callbacks
from src.detection.deep.training.Crosswalk_dataset import Crosswalk_dataset

'''
Attention: The Keras library changes all the time. You can't be sure the interface will be changed tomorrow! Use the keras library on the delivered CD.
'''
def load_dataset(sourcefolder, split_factor):
    dataset = Crosswalk_dataset.from_sourcefolder(sourcefolder)
    dataset.read_samples()
    dataset.load_images()
    (train_set, test_set) = dataset.split_train_test(split_factor)
    _print_dataset_details(dataset, train_set, test_set)
    return (train_set.to_input_response(), test_set.to_input_response())

def _print_dataset_details(dataset, train_set, test_set):
    print("Loaded ", len(dataset.samples_shuffled), " images")
    print(len(dataset.samples_crosswalk.samples), " crosswalks")
    print(len(dataset.samples_nocrosswalk.samples), " noncrosswalks")
    print(len(train_set.samples_shuffled), " train samples")
    print(len(test_set.samples_shuffled), " test samples")

def compile_model():
    nb_classes = 2

    # input image dimensions
    img_rows, img_cols = 50, 50
    # number of convolutional filters to use
    nb_filters1 = 64
    nb_filters2 = 128
    nb_filters3 = 256
    # size of pooling area for max pooling
    nb_pool = 2
    # convolution kernel size
    nb_conv = 3
    #image is rgb
    img_channels = 3

    #Lamda for L2 regularization
    lmda = 3e-5


    print("put convnet together")
    model = Sequential()

    model.add(Convolution2D(nb_filters1, nb_conv , nb_conv, W_regularizer=l2(lmda), border_mode='full', input_shape=(img_channels, img_rows, img_cols)))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Convolution2D(nb_filters1, nb_conv, nb_conv, W_regularizer=l2(lmda)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))

    model.add(Dropout(0.5))
    model.add(Convolution2D(nb_filters2, nb_conv, nb_conv, W_regularizer=l2(lmda)))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Convolution2D(nb_filters2, nb_conv, nb_conv, W_regularizer=l2(lmda)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))

    model.add(Dropout(0.5))
    model.add(Convolution2D(nb_filters3, nb_conv, nb_conv, W_regularizer=l2(lmda)))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Convolution2D(nb_filters3, nb_conv, nb_conv, W_regularizer=l2(lmda)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))

    model.add(Flatten())

    model.add(Dropout(0.5))
    model.add(Dense(2048, W_regularizer=l2(lmda)))
    model.add(Activation('relu'))

    model.add(Dropout(0.5))
    model.add(Dense(1024, W_regularizer=l2(lmda)))
    model.add(Activation('relu'))

    model.add(Dropout(0.5))
    model.add(Dense(nb_classes, W_regularizer=l2(lmda)))
    model.add(Activation('softmax'))

    print("start compiling")
    model.compile(loss='categorical_crossentropy', optimizer='adadelta')
    #model.load_weights("kerasSerialization/convnet55_3.e63-l0.062_valacc0.9809.hdf5")
    return model

def create_train_callbacks(model_number):
    filepath = "kerasSerialization/convnet" + str(model_number) + ".e{epoch:02d}-l{val_loss:.3f}.hdf5"
    save_callback = ModelCheckpoint(filepath, verbose=1, save_best_only=True)
    early_stopping = EarlyStopping(monitor='val_loss', patience=50)
    remote = callbacks.RemoteMonitor(root='http://localhost:9000')
    return [early_stopping, save_callback, remote]

model_number = 55
sourcefolder = "dataset/"   # Path to dataset
split_factor = 0.95         # Factor to split dataset into train and testset. Trainset = 95%, testset = 5%
batch_size = 128
nb_epoch = 500              #M ax number of epochs.

# the data, shuffled and split between train and test sets
(X_train, Y_train), (X_test, Y_test) = load_dataset(sourcefolder, split_factor)

#Compile specific model
model = compile_model()

#Callbacks for training
# Early stopping    -> Stopps the training after x epochs with no progress
# Save callback     -> Saves the best model
# remote callback   -> Implements the connection to the hualos project (Keras visualization) Have a look on github
callbacks = create_train_callbacks(model_number)


# Train model with the parameter above
model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch, show_accuracy=True, verbose=1, validation_data=(X_test, Y_test), callbacks=callbacks)

