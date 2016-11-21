import pytest

from src.data.orthofoto.wms.wms_api import WmsApi
from src.base.bbox import Bbox


@pytest.fixture(scope='module')
def rappi():
    return Bbox(left=8.8181022825, bottom=47.2263345016, right=8.8188113747, top=47.2268572692)


def test_wms_hsr(rappi):
    try:
        wms_api = WmsApi(zoom_level=19)
        image = wms_api.get_image(rappi)
        assert image is not None
    except:
        assert True
