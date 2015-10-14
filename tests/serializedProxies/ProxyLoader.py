from src.service.TilesLoader.TileProxy import TileProxy
from src.base.Constants import Constants
class ProxyLoader:

    @staticmethod
    def load(filename):
        TileProxy.fromFile(Constants.SerializationFolder + filename)
