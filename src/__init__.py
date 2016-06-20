import environ
import os

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

root = environ.Path(os.getcwd())
cwenv = environ.Env(
    REDIS_HOST=(
        str,
        'db'),
    REDIS_PORT=(
        str,
        '6379'),
    REDIS_PASS=(
        str,
        'crosswalks'),
    REDIS_JOBQUEUE_NAME=(
        str,
        'jobs'),
    MAPQUEST_API_KEY=(
        str,
        'Undefined'),
    CONVNET_WEIGHTS_FILE=(
        environ.Path,
        root('src/detection/deep/convnet48.e158-l0.055.hdf5')),
    OUTPUT_DIR=(
        str,
        '.'),
)
environ.Env.read_env(root('.env'))  # reading .env file
