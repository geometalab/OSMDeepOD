# OSM-Crosswalk-Detection

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.md)

## Docker image for OSM-Crosswalk-Detection

This image is used for the OSM-Crosswalk-Detection project.
You can directly start the different worker roles described in the next paragraph.

## How to use

```bash
#Manager
docker run murthy10/osm-crosswalk-detection REDIS_IP_ADDR --role manager left bottom right top

#Jobworker
docker run murthy10/osm-crosswalk-detection REDIS_IP_ADDR --role resultworker

#Resultworker
docker run murthy10/osm-crosswalk-detection REDIS_IP_ADDR --role jobworker
```
