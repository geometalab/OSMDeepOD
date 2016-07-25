FROM docker pull tensorflow/tensorflow
MAINTAINER Samuel Kurath <samuel.kurath@hsr.ch>

RUN apt-get update \
  && apt-get install --no-install-recommends -y \
  libhdf5-dev \
  python-yaml \
  python-pil \
  && apt-get autoclean autoremove clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /root
