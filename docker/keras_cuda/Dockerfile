FROM geometalab/theano_cuda:latest
MAINTAINER Marcel Huber <marcel.huber@hsr.ch>
#Bases on https://github.com/Kaixhin/dockerfiles/blob/master/cuda-keras/cuda_v7.5/Dockerfile

# Install dependencies
RUN apt-get update && apt-get --no-install-recommends install -y \
  libhdf5-dev \
  python-h5py \
  python-yaml \
  && apt-get autoclean autoremove \
  && rm -rf /var/lib/apt/lists/*

# Upgrade six
RUN pip install --upgrade six

# Clone Keras repo and move into it
RUN cd /root && git clone https://github.com/fchollet/keras.git && cd keras && \
  # Install
  python setup.py install

# Set ~/keras as working directory
WORKDIR /root/keras

