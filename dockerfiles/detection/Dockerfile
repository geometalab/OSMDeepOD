FROM nvidia/cuda:7.5-cudnn4-devel-ubuntu14.04

MAINTAINER Samuel Kurath <skurath@hsr.ch>

RUN apt-get update \
&& apt-get upgrade -y \
&& apt-get install -y python3-pip python3-dev python3 git vim libjpeg-dev libjpeg8-dev libgdal1-dev\
&& export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow-0.10.0rc0-cp34-cp34m-linux_x86_64.whl \
&& pip3 install --upgrade pip \
&& pip install --upgrade $TF_BINARY_URL \
&& cd / \
&& git clone https://github.com/geometalab/OSM-Crosswalk-Detection.git \
&& cd OSM-Crosswalk-Detection \
&& pip uninstall requests -y \
&& pip install -r requires.dev.txt \
&& python3 setup.py install \

