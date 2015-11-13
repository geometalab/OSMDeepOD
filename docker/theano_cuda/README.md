# Theano_cuda

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.md)

## Theano docker image for nvidia-docker

This image bases on the docker file of kaixhin/cuda-theano, but instead of his own cuda image, this image implements the experimental nvidia-docker image.

The nvidia-docker project gives you the advantage that you don't need the same cuda driver in your docker container like on your host.

## How to use

```bash
# Download the nvidia-docker project
git clone https://github.com/NVIDIA/nvidia-docker.git
cd nvidia-docker

# Pull this image
docker pull sebu/theano_cuda
# Start container and mount GPU 0
GPU=0 ./nvidia-docker run -i -t sebu/theano_cuda
```

## Further informations
- [Experimental nvidia-docker project](https://github.com/NVIDIA/nvidia-docker "")
- [Kaixhin cuda-theano image](https://hub.docker.com/r/kaixhin/cuda-theano/ "")


