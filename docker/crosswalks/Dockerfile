FROM geometalab/keras_cuda:latest
MAINTAINER Marcel Huber <marcel.huber@hsr.ch>

RUN pip install --upgrade \
  nose

RUN cd /root \
  && git clone --single-branch --branch master --depth 1 https://github.com/geometalab/OSM-Crosswalk-Detection.git \
  && cd OSM-Crosswalk-Detection \
  && python setup.py install \
  && touch DockerIam

ENTRYPOINT [ "python", "/root/OSM-Crosswalk-Detection/src/role/main.py", "--redis" ]

WORKDIR /root/OSM-Crosswalk-Detection

