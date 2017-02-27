FROM nvidia/cuda:8.0-runtime-ubuntu14.04

MAINTAINER Samuel Kurath <skurath@hsr.ch>

RUN apt-get update \
&& apt-get install wget -y \
&& wget -qO - http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1404/x86_64/7fa2af80.pub | sudo apt-key add - \
&& apt-get update \
&& apt-get upgrade -y \
&& apt-get install -y python3-pip python3-dev python3 git vim libjpeg-dev libjpeg8-dev \
&& cd / \
&& git clone https://github.com/geometalab/OSMDeepOD.git \
&& cd OSMDeepOD \
&& pip3 uninstall requests -y \
&& pip3 install -r requires.dev.txt \
&& sudo pip3 install --upgrade  https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.0.0-cp34-cp34m-linux_x86_64.whl \
&& python3 setup.py install \

