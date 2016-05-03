[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.md)

# Docker images

This project provides 4 docker images. Three images to train a convnet and one image to execute and distribute the recognition work.
The images are automatically built and pushed by circleci. You can pull them using the following links:
- [osm_crosswalk_detection - Recognition image](https://hub.docker.com/r/geometalab/osm-crosswalk-detection/ "")
- [keras_cuda - Training image](https://hub.docker.com/r/geometalab/keras_cuda/ "")
- [theano_cuda](https://hub.docker.com/r/geometalab/theano_cuda/ "")
- hualos_keras_cuda (obsolete)


## How to use the images?

Have a look on the README.md in the specific folders or read the *Using docker images* section of the README.md in the parent folder.


## Build the images locally

After having modified the source tree and probably before wanting to publish the changes, it would be nice and wise to test if the resulting docker image works as expected.
Creating such a docker image requires an url and a branch to your modified repository.
In the following example I will export the current repository I am working on as I do not want to push it to the remote yet.

1. Commit your changes onto a feature branch

   ```
   git checkout -b SuperDuper
   git commit -a -m"modified X and Y"
   ```

2. Expose the repository for cloning

   ```
   git daemon --export-all --verbose $(pwd) &
   ```
   `git` allow us to export the current working dir and make it cloneable.

3. Build the docker image

   Here I use `crane` again as I already prepared the `crosswalk` container to being provisioned. I need to setup `GIT_REPO_URL` and `GIT_BRANCH` to point to the git URL and branch of the local daemon:
   ```
   GIT_REPO_URL=git://$(hostname):9418/$(pwd) GIT_BRANCH=SuperDuper crane --verbose --config=docker/crane.yaml provision crosswalk
   ```

4. Test the image

   To test the image, we run the tests inside the image as circleci would do it too:
   ```
   MAPQUEST_API_KEY="Your API Key Here" crane --verbose --config=docker/crane.yaml run ctests
   ```