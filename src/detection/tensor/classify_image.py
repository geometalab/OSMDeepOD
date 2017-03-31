import argparse
import os
from PIL import Image

from src.detection.tensor.detector import Detector


def check_file(file_path):
    if not os.path.isfile(file_path):
        raise Exception("File {0} does not exist!".format(file_path))


def main_function():
    parser = argparse.ArgumentParser(description='Test a trained neuronal network.', )
    parser.add_argument(
        '-i',
        '--image',
        action='store',
        dest='image',
        required=True,
        help='The path to the input image file.'
    )
    parser.add_argument(
        '-g',
        '--graph',
        action='store',
        dest='graph',
        required=True,
        help='The path to the graph file.'
    )

    parser.add_argument(
        '-l',
        '--label',
        action='store',
        dest='label',
        required=True,
        help='The path to the label file.'
    )

    args = parser.parse_args()

    for key, value in vars(args).items():
        check_file(value)

    detector = Detector(graph_file=args.graph, labels_file=args.label)
    image = Image.open(args.image)

    answer = detector.detect([image])
    print(answer)


if __name__ == "__main__":
    main_function()
