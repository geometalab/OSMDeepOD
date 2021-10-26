FROM jupyter/scipy-notebook:lab-3.2.0 as default

USER root

RUN apt-get update \
    && apt-get install -y \
    wget \
    git \
    vim \
    gdal-bin \
    && rm -rf /var/lib/apt/lists/*

RUN mamba install --quiet -c fastchan -y fastai \
    && mamba clean -tipsy \
    && fix-permissions "${CONDA_DIR}" \
    && fix-permissions "/home/${NB_USER}"

RUN  mamba install --quiet -c conda-forge -y \
    pyrosm \
    pyarrow \
    sidecar \
    ipyleaflet \
    ipyvuetify \
    xarray_leaflet \
    voila \
    voila-gridstack \
    && mamba clean -tipsy \
    && fix-permissions "${CONDA_DIR}" \
    && fix-permissions "/home/${NB_USER}"

RUN pip install  --quiet --no-cache-dir \
    rasterio \
    turfpy \
    fiona \
    shapely \
    xarray \
    tifffile \
    && fix-permissions "${CONDA_DIR}" \
    && fix-permissions "/home/${NB_USER}"

USER $NB_USER
# COPY --chown=${NB_ID}:${NB_ID} . /OSMDeepOD



# kept just for posterity
FROM tensorflow/tensorflow:2.6.0-gpu-jupyter as gpu-old

RUN apt-get update \
    && apt-get install -y \
    wget \
    git \
    vim \
    libjpeg-dev \
    libjpeg8-dev

WORKDIR /OSMDeepOD
COPY . /OSMDeepOD

RUN pip3 uninstall -y requests \
    && pip3 install -r requires.dev.txt
