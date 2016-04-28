FROM skydjol/nvidia-docker:latest
MAINTAINER Marcel Huber <marcel.huber@hsr.ch>
#Bases on https://github.com/Kaixhin/dockerfiles/blob/master/cuda-theano/cuda_v7.5/Dockerfile

RUN apt-get update && apt-get upgrade -y && \
  apt-get install --no-install-recommends -y \
  git \
  libopenblas-dev \
  python-dev \
  python-pip \
  python-scipy \
  && apt-get autoclean autoremove clean \
  && rm -rf /var/lib/apt/lists/*

RUN pip install \
  "Theano==0.8.2"

# Set CUDA_ROOT
ENV CUDA_ROOT /usr/local/cuda/bin
# Set up .theanorc for CUDA
RUN echo "[global]\ndevice=gpu\nfloatX=float32\n[nvcc]\nfastmath=True" > /root/.theanorc
