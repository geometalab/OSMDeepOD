FROM geometalab/theano_cuda:latest
MAINTAINER Marcel Huber <marcel.huber@hsr.ch>
#Bases on https://github.com/Kaixhin/dockerfiles/blob/master/cuda-keras/cuda_v7.5/Dockerfile

RUN apt-get update && \
  apt-get install --no-install-recommends -y \
  libhdf5-dev libyaml-0-2 && \
  apt-get autoclean autoremove clean && \
  rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade \
  h5py PyYAML "Keras==1.0.1"

WORKDIR /root
