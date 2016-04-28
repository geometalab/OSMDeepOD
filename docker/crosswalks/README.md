# OSM-Crosswalk-Detection

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.md)

## Docker image for OSM-Crosswalk-Detection

This image is used for the OSM-Crosswalk-Detection project.
You can directly start the different worker roles described in the next paragraph.

## How to use

Specifying `--redis`, `--port`, `--pass` is optional when using the following example setup.

```bash
#Redis, start instance
docker run --name crossdis redis:alpine

#Redis, setup redis password
# -> Redo this everytime if redis is not persisting its data
docker run --rm --link crossdis:db redis:alpine /bin/sh -c 'printf "config set requirepass crosswalks\nauth crosswalks\n" | redis-cli -h db'

#Manager, example zurich bellevue
docker run --rm --link crossdis:db geometalab/osm-crosswalk-detection --redis db manager 8.54279671719532 47.366177501999516 8.547088251618977 47.36781249586627

#Jobworker
docker run --rm --link crossdis:db geometalab/osm-crosswalk-detection jobworker

#Resultworker
docker run --rm --link crossdis:db --volume /localoutput:/output:rw geometalab/osm-crosswalk-detection resultworker
```
