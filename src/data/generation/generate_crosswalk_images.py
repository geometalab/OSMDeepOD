import os
import argparse
import csv

from src.base.bbox import Bbox
from src.data.generation.crosswalk_collector import CrosswalkCollector


def collect(bboxes, args):
    crosswalk_collector = CrosswalkCollector(image_dir=args.image_dir)
    for bbox in bboxes:
        crosswalk_collector.bbox = bbox
        crosswalk_collector.run()


def run(args):
    bboxes = []
    if args.csv is not None:
        if os.path.exists(args.csv):
            with open(args.csv, 'rb') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                next(reader)
                for row in reader:
                    bbox = Bbox.from_lbrt(float(row[1]), float(row[2]), float(row[3]), float(row[4]))
                    bboxes.append(bbox)
        else:
            raise Exception('CSV file ' + args.csv + ' does not exist!')
    else:
        bboxes.append(Bbox.from_lbrt(args.bbox[0], args.bbox[1], args.bbox[2], args.bbox[3]))
    collect(bboxes, args)


def mainfunc():
    parser = argparse.ArgumentParser(description='Generate crosswalk images.', )
    parser.add_argument(
            '-b',
            '--bbox',
            nargs=4,
            action='store',
            dest='bbox',
            help='The boundingbox to look for crosswalks. (left, bottom, right, top)',
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
            '--csv',
            action='store',
            dest='csv',
            help='The path to the csv bounding box file. (csv: region, left, bottom, right, top)'
    )

    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    mainfunc()
