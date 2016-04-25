[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Codacy Badge](https://api.codacy.com/project/badge/grade/05519d68c18145d6a885276e70cb6770)](https://www.codacy.com/app/samuel-kurath/OSM-Crosswalk-Detection)
[![Circle CI](https://circleci.com/gh/geometalab/OSM-Crosswalk-Detection.svg?style=svg)](https://circleci.com/gh/geometalab/OSM-Crosswalk-Detection)
[![Stories in Ready](https://badge.waffle.io/geometalab/OSM-Crosswalk-Detection.svg?label=ready&title=Ready)](http://waffle.io/geometalab/OSM-Crosswalk-Detection)


# OSM-Crosswalk-Detection: Deep learning based image recognition

## Introduction

OSM-Crosswalk-Detection is a highly scalable image recognition software for aerial photos (orthophotos). It uses the deep learning library Keras, more precisely a VGGNet like convolutional neural network, to detect crosswalks along streets.
This Python based project provides a Keras docker container to train the neural network on a GPU and several docker containers to distribute the recognition work on multiple servers.

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

## Links
- http://wiki.hsr.ch/StefanKeller/SA_BA_Gamified_Extraction_of_Crosswalks_from_Aerial_Images
- www.hsr.ch
- www.osm.org
- www.maproulette.org

