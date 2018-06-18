from src.base.tile import Tile
from src.base.bbox import Bbox
from src.base.node import Node
from src.base.tag import Tag

from src.data.orthofoto.wms.wms_api import WmsApi

from src.train.coord_walker import CoordWalker
from src.train.osm_object_walker import OsmObjectWalker

import argparse

def main(args):
    coords = list(map(lambda c: Node(*map(float, c.split(','))), args.coord))
    bbox = Bbox.from_nodes(coords[0], coords[1])
    if args.tags:
        tags = map(lambda k, v: Tag(key=k, value=v), map(lambda kv: kv.split('=', 1), args.tags.split(',')))
        #walker = OsmObjectWalker(Tile(image_api=WmsApi(), bbox=bbox), Tag(key='public_transport', value='platform'), square_image_length=100)
        walker = OsmObjectWalker(Tile(image_api=WmsApi(), bbox=bbox), tags, square_image_length=100)
    else:
        walker = CoordWalker(Tile(image_api=WmsApi(), bbox=bbox), coords, square_image_length=100)

    tiles = walker.get_tiles()
    for n, t in enumerate(tiles):
        centre_node = t.get_centre_node()
        name = "fetch/{0:02.8}_{1:02.8}.png".format(centre_node.latitude, centre_node.longitude)
        t.image.save(name, "PNG")
        print(name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--tags',
        type=str,
        default=None,
        help='Tag to fetch from OSM: highway=crossing.'
    )

    parser.add_argument(
        'coord',
        type=str,
        action='store',
        nargs='+',
        help='lon,lat coord in WGS84, if --tags bbox left,bottom right,top, else list of coords to fetch.')

    args = parser.parse_args()
    main(args)

# mapproxy-util serve-develop mapproxy.yml
# montage *.png -geometry 100x100+1+1 out.png
# python retrain.py --image_dir retrain-data --print_misclassified_test_images
