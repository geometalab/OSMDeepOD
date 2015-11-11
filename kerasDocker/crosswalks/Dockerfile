FROM sebu/keras_cuda:latest
MAINTAINER Samuel Kurath <skurath@hsr.ch>

# Clone 
RUN cd /root 
RUN git clone https://github.com/geometalab/OSM-Crosswalk-Detection.git
RUN cd OSM-Crosswalk-Detection
RUN python setup.py install

# Set ~/OSM-Crosswalk-Detection as working directory
WORKDIR /root/OSM-Crosswalk-Detection
