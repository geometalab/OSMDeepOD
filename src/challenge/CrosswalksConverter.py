import argparse
import json
import uuid
import os


def addcsvelt(json_data, input_filename):
    def build_element(crosswalk):
        return str(
            crosswalk['latitude']) + ',' + str(crosswalk['longitude']) + os.linesep

    elements = [build_element(crosswalk)
                for crosswalk in json_data['crosswalks']]
    value = 'latitude,longitude' + os.linesep + ''.join(elements)
    output_filename = os.path.splitext(input_filename)[0] + '.csv'
    with open(output_filename, 'w') as f:
        f.write(value)


def convert_maproulette(json_data, input_filename):
    def build_element(crosswalk):
        element = \
            {
                "geometries": {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "properties": {
                            },
                            "geometry": {
                                "type": "Point",
                                "coordinates": [
                                    crosswalk['longitude'],
                                    crosswalk['latitude']
                                ]
                            }
                        }
                    ]
                },
                "identifier": str(uuid.uuid4())
            }
        return element

    elements = [build_element(crosswalk)
                for crosswalk in json_data['crosswalks']]
    value = str(elements).replace("'", '"')
    output_filename = 'tasks.json'
    with open(output_filename, 'w') as f:
        f.write(value)


def convert_geojson(json_data, input_filename):
    def build_element(crosswalk):
        element = \
            {
                "type": "Feature",
                "properties": {
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        crosswalk['longitude'],
                        crosswalk['latitude']
                    ]
                }
            }
        return element

    outer = \
        {
            "type": "FeatureCollection",
            "features": [
            ]
        }
    outer['features'] = [build_element(crosswalk)
                         for crosswalk in json_data['crosswalks']]
    value = str(outer).replace("'", '"')
    output_filename = os.path.splitext(input_filename)[0] + '.geo.json'
    with open(output_filename, 'w') as f:
        f.write(value)


def convert(args):
    data = json.load(args.input_file)
    data_filename = args.input_file.name
    for conv_func in args.conversion_funcs:
        conv_func(data, data_filename)


def mainfunc():
    parser = argparse.ArgumentParser(
        description='Convert crosswalks json to other formats',
    )
    parser.add_argument(
        '--csv',
        action='append_const',
        dest='conversion_funcs',
        const=addcsvelt,
        help='convert to csv format with two columns [latitude,longitude]')
    parser.add_argument(
        '--geojson',
        action='append_const',
        dest='conversion_funcs',
        const=convert_geojson,
        help='convert to geojson format')
    parser.add_argument(
        '--maproulette',
        action='append_const',
        dest='conversion_funcs',
        const=convert_maproulette,
        help='convert to maproulette.org challenge format')
    parser.add_argument(
        'input_file',
        type=file,
        help='name of crosswalks json file')
    parser.set_defaults(func=convert)

    args = parser.parse_args()
    if args.conversion_funcs is not None:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    mainfunc()
