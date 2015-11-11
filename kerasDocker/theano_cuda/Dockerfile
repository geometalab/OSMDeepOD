FROM skydjol/nvidia-docker:latest
MAINTAINER Severin Bühler <sbuehler@hsr.ch>
#Bases on https://github.com/Kaixhin/dockerfiles/blob/master/cuda-theano/cuda_v7.5/Dockerfile

# Install git, python-dev, pip and other dependencies
RUN apt-get update && apt-get install -y \
  git \
  libopenblas-dev \
  python-dev \
  python-pip \
  python-nose \
  python-numpy \
  python-scipy

# Set CUDA_ROOT
ENV CUDA_ROOT /usr/local/cuda/bin
# Install bleeding-edge Theano
RUN pip install --upgrade --no-deps git+git://github.com/Theano/Theano.git
# Set up .theanorc for CUDA
RUN echo "[global]\ndevice=gpu\nfloatX=float32\n[nvcc]\nfastmath=True" > /root/.theanorc