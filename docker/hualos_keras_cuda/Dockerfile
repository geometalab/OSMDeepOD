FROM keras_cuda7.5
MAINTAINER Marcel Huber <marcel.huber@hsr.ch>
# Based on https://github.com/fchollet/hualos

# Install dependencies
RUN pip install Flask
RUN pip install gevent

# Install hualos visualization for keras
RUN git clone https://github.com/fchollet/hualos.git && cd hualos

# Make port public for hualos
EXPOSE 9000:9000

# Set ~/keras as working directory
WORKDIR /root/keras
