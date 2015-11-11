FROM sebu/keras_cuda:latest
MAINTAINER Samuel Kurath <skurath@hsr.ch>
Dockerfile

# Clone 
RUN cd /root && git clone https://github.com/geometalab/OSM-Crosswalk-Detection.git && cd OSM-Crosswalk-Detection && \
  # Install
  python setup.py install

# Set ~/OSM-Crosswalk-Detection as working directory
WORKDIR /root/OSM-Crosswalk-Detection
