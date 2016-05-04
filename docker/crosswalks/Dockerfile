FROM geometalab/keras_cuda:latest
MAINTAINER Marcel Huber <marcel.huber@hsr.ch>

RUN apt-get update \
  && apt-get install --no-install-recommends -y xloadimage \
  && apt-get autoclean autoremove clean \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade \
  nose django-environ coverage codacy-coverage

ARG GIT_BRANCH
ARG GIT_REPO_URL
ENV GIT_BRANCH=${GIT_BRANCH:-master} \
    GIT_REPO_URL=${GIT_REPO_URL:-https://github.com/geometalab/OSM-Crosswalk-Detection.git}

RUN echo "repo URL:[$GIT_REPO_URL] branch:[$GIT_BRANCH]"

RUN cd /root \
  && git clone --single-branch --branch $GIT_BRANCH --depth 1 $GIT_REPO_URL \
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
