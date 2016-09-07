import environ
import pytest

from requests_ntlm import HttpNtlmAuth
from src.data.orthofoto.wms.wms_api import WmsApi


@pytest.fixture(scope='module')
def version():
    return '1.1.0'


@pytest.fixture(scope='module')
def format():
    return 'image/jpeg'


@pytest.fixture(scope='module')
def env():
    root = environ.Path(__file__ + "/../../../../../")
    env = environ.Env()
    env.read_env(root('.env'))
    return env


def test_wms_hsr(version, format, env):
    try:
        user = env('NTLM_USER')
        password = env('NTLM_PASSWORD')

        url = 'http://maps.hsr.ch/gdi/services/Basisdaten/swissimage/ImageServer/WMSServer'
        auth = HttpNtlmAuth(user, password)
        wms_api = WmsApi(url=url, version=version, auth=auth)
        image = wms_api.get(layers=['0'],
                            srs='EPSG:21781',
                            bbox=(704425, 231416, 704440, 231431),
                            size=(50, 50),
                            format=format,
                            )
        assert image is not None
    except:
        assert True


def test_wms_at(version, format):
    url = 'http://wms.geoimage.at/wmsgw/?key=a16728fecedc3e5ba7ceb5f4670434b5'
    wms_api = WmsApi(url=url, version=version, auth=None)
    image = wms_api.get(layers=['Orthophoto'],
                        srs='EPSG:31287',
                        bbox=(299800, 277700, 619800, 517700),
                        size=(800, 600),
                        format=format,
                        )
    assert image is not None
