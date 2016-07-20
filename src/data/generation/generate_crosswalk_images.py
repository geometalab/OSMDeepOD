import argparse

from src.base.Bbox import Bbox
from src.data.generation.crosswalk_collector import CrosswalkCollector


def run(args):
    bbox = Bbox.from_lbrt(args.bbox[0], args.bbox[1], args.bbox[2], args.bbox[3])
    crosswalkCollector = CrosswalkCollector(bbox=bbox, hdf5_file=args.convnet, image_dir=args.image_dir)
    crosswalkCollector.run()


def mainfunc():
    parser = argparse.ArgumentParser(description='Generate crosswalk images.', )
    parser.add_argument(
            '-b',
            '--bbox',
            nargs=4,
            action='store',
            dest='bbox',
            help='The boundingbox to look for crosswalks. (left, bottom, right, top)',
            required=True
    )

    parser.add_argument(
            '-i',
            '--image_dir',
            action='store',
            dest='image_dir',
            help='The destination for the found crosswalk images.',
            required=True
    )

    parser.add_argument(
            '-c',
            '--convnet',
            action='store',
            dest='convnet',
            help='The path to the convnet file. (inclusive filename)'
    )

    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    mainfunc()
