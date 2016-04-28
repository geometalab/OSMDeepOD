FROM geometalab/keras_cuda:latest
MAINTAINER Marcel Huber <marcel.huber@hsr.ch>

RUN pip install --upgrade \
  nose django-environ

ARG CIRCLE_BRANCH
ENV CIRCLE_BRANCH ${CIRCLE_BRANCH:-master}

RUN cd /root \
  && git clone --single-branch --branch $CIRCLE_BRANCH --depth 1 https://github.com/geometalab/OSM-Crosswalk-Detection.git \
  && cd OSM-Crosswalk-Detection \
  && python setup.py install \
  && touch DockerIam

# store results in this directory
ENV OUTPUT_DIR=/output

# map this drive externally to persist results
VOLUME ["$OUTPUT_DIR"]

ENTRYPOINT [ "python", "/root/OSM-Crosswalk-Detection/src/role/main.py" ]
CMD [ "--help" ]

WORKDIR /root/OSM-Crosswalk-Detection
