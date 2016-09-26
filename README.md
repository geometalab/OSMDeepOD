[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Codacy Badge](https://api.codacy.com/project/badge/grade/6d2ec33de73d4f929dfab6c0f186f1d7)](https://www.codacy.com/app/marcelhuberfoo/OSM-Crosswalk-Detection)
[![Build Status](https://travis-ci.org/geometalab/OSM-Crosswalk-Detection.svg?branch=master)](https://travis-ci.org/geometalab/OSM-Crosswalk-Detection)
[![Stories in Ready](https://badge.waffle.io/geometalab/OSM-Crosswalk-Detection.svg?label=ready&title=Ready)](http://waffle.io/geometalab/OSM-Crosswalk-Detection)


# OSM-Crosswalk-Detection: Deep learning based image recognition

## Introduction

OSM-Crosswalk-Detection is a highly scalable image recognition software for aerial photos (orthophotos). It uses the open source software library TensorFlow, with a retrained Inception V3 neuronal network, to detect crosswalks along streets.

This work started as part of a semester thesis autumn 2015 at Geometa Lab, University of Applied Sciences Rapperswil (HSR).

## Overview

![Marcitecture](http://s11.postimg.org/7bdx1cetf/SA_Overview_new.png)

## Examples
![Detection-Example1](imgs/preview_crosswalk_rappi2.png)

Picture 1: Rapperswil trainstation (47.226468, 8.818477)

![Detection-Example2](imgs/preview_crosswalk_rappi.png)

Picture 2: Rapperswil residential (47.232803, 8.837321)

## Dataset
During this work, we have collected our own dataset with swiss crosswalks and non-crosswalks. The pictures have a size of 50x50 pixels and are available by request.

![Crosswalk Examples](imgs/Zebrastreifen_examples.png)

Picture 3: Crosswalk Examples

![No-Crosswalk Examples](imgs/No_Zebrastreifen_examples.png)

Picture 4: No Crosswalk Examples

## Getting Started

### Prerequisites

- Python

  At the moment, we support python 3.x

- Docker

  In order to use volumes, I recommend using docker >= 1.9.x

- Bounding Box of area to analyze

  To start the extraction of crosswalks within a given area, the bounding box of this area is required as arguments for the manager. To get the bounding box the desired area, you can use https://www.openstreetmap.org/export to select the area and copy paste the corresponding coordinates. Use the values in the following order when used as positional arguments to manager: `left bottom right top`

### Usage
The simplest way to use the detection process is to clone the repository and build/start the docker containers.

```
git clone https://github.com/geometalab/OSM-Crosswalk-Detection.git
cd OSM-Crosswalk-Detection/dockerfiles/
sudo python docker_run.py -r -d
```

After the previous shell commands you have started a redis instance for data persistance and a container for the detection process.
Now you should be connected to a tty of the crosswalk_detection container. If you have a nvida GPU and nvidia-docker installed the detection algorithm will automatically use this GPU<sup id="a1">[1](#GPU)</sup>.

To start the detection process use the src/role/main.py<sup id="a2">[2](#main)</sup> script.

1. Use the manger option to select the detection area and generate the jobs stored by the redis instance
```
python3 main.py --redis 172.17.0.25 --port 40001 --pass crosswalks manager 9.345101 47.090794 9.355947 47.097288 --tag junction roundabout --search roundabout --no_compare --zoom_level 17 --orthofoto other
```
The default settings of --tag, --search, and --zoom_level are for crosswalk detection.
The parameter '--orthofoto' is for the image source. (More under 'Own Orthofotos')


2. Start the detection algorithm. The results are also stored by the redis instance.
```
python main.py --redis 127.0.0.1 --port 40001 --pass crosswalks jobworker
```

3. Collect the results in a simple JSON file.
```
python main.py --redis 127.0.0.1 --port 40001 --pass crosswalks resultworker
```

If you have execute the result worker in the docker container you can move the crosswalks.json file to the /crosswalk/ directory which is map to your host.



### Own Orthofotos
To use your own Orthofotos you have to do the following steps:

    1. Add a new directory to src/data/orthofoto
    2. Add a new module to the directory with the name: 'your_new_directory'_api.py
    3. Create a class in the module with the name: 'Your_new_directory'Api   (First letter needs to be uppercase)
    4. Implement the function 'def get_image(self, bbox):' and returns a pillow image of the bbox
    5. After that you can use your api with the parameter --orthofots 'your_new_directory'

If you have problems with the implementation have a look at the wms or other example.

## Links
- http://wiki.hsr.ch/StefanKeller/SA_BA_Gamified_Extraction_of_Crosswalks_from_Aerial_Images
- www.hsr.ch
- www.osm.org
- www.maproulette.org


## Notes
<a name="GPU">1</a>: The crosswalk_detection container is based on the nvidia/cuda:7.5-cudnn4-devel-ubuntu14.04 image, may you have to change the base image for your GPU. [↩](#a1)
<a name="main">2</a>: For more information about the main.py use the -h option. [↩](#a2)
