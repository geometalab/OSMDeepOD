[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Codacy Badge](https://api.codacy.com/project/badge/grade/8bd24fe19ffb4c3ea0e947225e962d28)](https://www.codacy.com/app/samuel-kurath/OSM-Crosswalk-Detection/dashboard)

# OSM-Crosswalk-Detection: Deep learning based image recognition

## You just have found this project

OSM-Crosswalk-Detection is a high scalable image recognition software for aerial photos (orthophotos). It uses the deep learning library Keras, more precisely a VGGNet like convolutional neural network, to detect crosswalks along streets.
This python based project provides a keras docker container to train the neural network on a gpu and  several docker container to distribute the recognition work on multiple servers.

This work is part of the semester thesis at the university of applied science Rapperswil (HSR).

## Overview

![Marcitecture](http://s11.postimg.org/7bdx1cetf/SA_Overview_new.png)

## Examples
![Detection-Example1](imgs/preview_crosswalk_rappi2.png)

Rapperswil trainstation (47.226468, 8.818477)

![Detection-Example2](imgs/preview_crosswalk_rappi.png)

Rapperswil suburb (47.232803, 8.837321)



## Further informations
http://wiki.hsr.ch/StefanKeller/SA_BA_Gamified_Extraction_of_Crosswalks_from_Aerial_Images

## Links
- www.hsr.ch
- www.osm.org
- www.maproulette.org

