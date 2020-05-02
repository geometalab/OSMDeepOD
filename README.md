[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Codacy Badge](https://api.codacy.com/project/badge/grade/6d2ec33de73d4f929dfab6c0f186f1d7)](https://www.codacy.com/app/marcelhuberfoo/OSM-Crosswalk-Detection)
[![Build Status](https://travis-ci.org/geometalab/OSMDeepOD.svg?branch=master)](https://travis-ci.org/geometalab/OSMDeepOD)
[![Stories in Ready](https://badge.waffle.io/geometalab/OSM-Crosswalk-Detection.svg?label=ready&title=Ready)](http://waffle.io/geometalab/OSM-Crosswalk-Detection)


#  OSMDeepOD - OSM and Deep Learning based Object Detection from Aerial Imagery 

OSMDeepOD is a project about object detection from aerial imagery using open data from OpenStreetMap (OSM).
The project uses the open source software library TensorFlow, with a retrained Inception V3 neuronal network.

This work started as part of a semester thesis autumn 2015 at Geometa Lab, University of Applied Sciences Rapperswil (HSR). See [Twitter hashtag #OSMDeepOD](https://twitter.com/hashtag/OSMDeepOD) for news.

## Material and Publications
 * Part of KTI innovation check 2017/2018.
 * "OSMDeepOD - Object Detection on Orthophotos with and for VGI2, by Samuel Kurath, Raphael Das Gupta and Stefan Keller. GI_Forum 2017, Issue 2, pages 173 -188, [DOI: 10.1553/giscience2017_02_s173](https://doi.org/10.1553/giscience2017_02_s173). Web: http://hw.oeaw.ac.at/0xc1aa500e%200x00373589.pdf (Jan 2018)
 * Keller S., Bühler S., Kurath S. (2018): Erkennung von Fußgängerstreifen aus Orthophotos. AGIT 2016, 7.7.2016. [online](http://gispoint.de/gisopen-paper/3875-erkennung-von-fussgaengerstreifen-aus-orthophotos/agit.html?IDjournalTitle=5&tx_browser_pi1[IDedition]=5)
 * Presentation (en) by S. Keller at GEOSmart Innovation Day 2016: tba.
 * [Presentation (en/de) by S. Bühler at PyDataZRH, 6.12.2016](https://twitter.com/SeverinBuhler/status/803193080211996672)

## Overview
![Detection-Example1](imgs/big_picture.png)

## Process
![Detection-Example1](imgs/process.png)

## Getting Started
The simplest way to use the detection process is to clone the repository and build/start the docker container.

```
git clone https://github.com/geometalab/OSMDeepOD.git
cd OSMDeepOD/docker/
sudo docker build . -t osmdeepod
sudo docker run -it --name osmdeepod -v ./:/objects osmdeepod bash
```

After the previous shell commands you have started a standalone instance of OSMDeepOD and you are connected to it.
If you have a nvida GPU and nvidia-docker installed, you could use the "nvidia-docker" command to run the container for automatically usage of the GPU<sup id="a1">[1](#GPU)</sup>.

To start the detection process use the src/role/main.py<sup id="a2">[2](#main)</sup> script.

1. Use the manger option to select the detection area and start the detection with the --standalone parameter.
```
python3 main.py --config ./config.ini --standalone manager 9.345101 47.090794 9.355947 47.097288
```

After the detection process has finished a "detected_nodes.json" file will appear with the results.
If you like to use OSMDeepOD in a more parallel and distributed way have a look at the https://github.com/geometalab/OSMDeepOD-Visualize repository.
There you have got the ability to use redis as a message queue and you can run many OSMDeepOD instances as workers.

### Configuration
The configuration works with an INI file.
The file looks like the following:
```
[DETECTION]
Network = /path/to/the/trained/convnet
Labels = /path/to/the/label/file/of/the/convnet
Barrier = 0.99
Word = crosswalk
Key = highway
Value = crossing
ZoomLevel = 19
Compare = yes
Orthofoto = wms
FollowStreets = yes
StepWidth = 0.66

[REDIS]
Server = 127.0.0.1
Port = 40001
Password = crosswalks

[JOB]
BboxSize = 2000
Timeout = 5400
```

Some hints to the config file:
 - "Word" is the key value of the labels file
 - "Key" and "Value" builds the search Tag for OSM
 - "Compare" means compared to OSM tagged Nodes
 - "StepWidth" regulates the distance between the cut out images
 - The section REDIS should be self explanatory, this is not necessary in the standalone mode
 - "BboxSize" is the size in meters of the split large Bbox
 - "Timeout" after the expired time the job does fail


### Own Orthofotos

Provide it as a WMS from a MapProxy server.

## Dataset
During this work, we have collected our own dataset with swiss crosswalks and non-crosswalks. The pictures have a size of 50x50 pixels and are available by request.

![Crosswalk Examples](imgs/Zebrastreifen_examples.png)

Picture 3: Crosswalk Examples

![No-Crosswalk Examples](imgs/No_Zebrastreifen_examples.png)

Picture 4: No Crosswalk Examples



## Prerequisites

- Python

  At the moment, we support python 3.5

- Docker

  In order to use volumes, I recommend using docker >= 1.9.x

- Bounding Box of area to analyze

  To start the extraction of crosswalks within a given area, the bounding box of this area is required as arguments for the manager. To get the bounding box the desired area, you can use https://www.openstreetmap.org/export to select the area and copy paste the corresponding coordinates. Use the values in the following order when used as positional arguments to manager: `left bottom right top`



## Links
- http://wiki.hsr.ch/StefanKeller/SA_BA_Gamified_Extraction_of_Crosswalks_from_Aerial_Images
- www.hsr.ch
- www.osm.org
- www.maproulette.org


## Notes
 - <a name="GPU">1</a>: The crosswalk_detection container is based on the nvidia/cuda:7.5-cudnn4-devel-ubuntu14.04 image, may you have to change the base image for your GPU. [↩](#a1)
 - <a name="main">2</a>: For more information about the main.py use the -h option. [↩](#a2)


## Keywords
Big Data; Data Science; Data Engineering; Machine Learning; Artificial Intelligence; Neuronal Nets; Imagery; Volunteered Geographic Information; Crowdsourcing; Geographic Information Systems; Infrastructure; Parallel Programming.
