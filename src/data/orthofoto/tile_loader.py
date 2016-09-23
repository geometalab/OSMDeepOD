from src.base.tile import Tile
from src.data.orthofoto.other.other_api import OtherApi


class TileLoader:
    def __init__(self, bbox=None, image_api=None):
        self.bbox = bbox
        self.image_api = OtherApi() if image_api is None else image_api
        self.tile = None

    def load_tile(self):
        image = self.image_api.get_image(self.bbox)
        self.tile = Tile(image, self.bbox)
        return self.tile
