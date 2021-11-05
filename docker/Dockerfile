# lab lab-3.2.x
FROM jupyter/scipy-notebook:ubuntu-20.04 as default

USER root

RUN apt-get update \
    && apt-get install -y \
    wget \
    git \
    vim \
    gdal-bin \
    gnupg2 \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

RUN mamba install --quiet -y -c fastchan \
    fastai \
    && mamba clean -tipsy \
    && fix-permissions "${CONDA_DIR}" \
    && fix-permissions "/home/${NB_USER}"

RUN mamba install --quiet -c conda-forge -y \
    nbconvert \
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
    "fastapi[all]" \
    nest_asyncio \
    && fix-permissions "${CONDA_DIR}" \
    && fix-permissions "/home/${NB_USER}"

USER $NB_USER
# COPY --chown=${NB_ID}:${NB_ID} . /OSMDeepOD

FROM default as cuda

USER root

#####################################################################################
## NVIDIA START

# from https://gitlab.com/nvidia/container-images/cuda/-/blob/master/dist/11.4.2/ubuntu2004/base/Dockerfile

ENV NVARCH x86_64
ENV NVIDIA_REQUIRE_CUDA "cuda>=11.4 brand=tesla,driver>=418,driver<419 brand=tesla,driver>=440,driver<441 brand=tesla,driver>=450,driver<451"
ENV NV_CUDA_CUDART_VERSION 11.4.108-1
ENV NV_CUDA_COMPAT_PACKAGE cuda-compat-11-4

ENV NV_ML_REPO_ENABLED 1
ENV NV_ML_REPO_URL https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/${NVARCH}

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gnupg2 ca-certificates wget curl \
    && curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/${NVARCH}/7fa2af80.pub | apt-key add - \
    && echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/${NVARCH} /" > /etc/apt/sources.list.d/cuda.list \
    && if [ ! -z ${NV_ML_REPO_ENABLED} ]; then echo "deb ${NV_ML_REPO_URL} /" > /etc/apt/sources.list.d/nvidia-ml.list; fi \
    && rm -rf /var/lib/apt/lists/*


ENV CUDA_VERSION 11.4.2

# For libraries in the cuda-compat-* package: https://docs.nvidia.com/cuda/eula/index.html#attachment-a
RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-cudart-11-4=${NV_CUDA_CUDART_VERSION} \
    ${NV_CUDA_COMPAT_PACKAGE} \
    && ln -s cuda-11.4 /usr/local/cuda && \
    rm -rf /var/lib/apt/lists/*

ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

RUN wget -O /NGC-DL-CONTAINER-LICENSE https://gitlab.com/nvidia/container-images/cuda/-/blob/master/NGC-DL-CONTAINER-LICENSE

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility

## NVIDIA END
#####################################################################################

USER $NB_USER
