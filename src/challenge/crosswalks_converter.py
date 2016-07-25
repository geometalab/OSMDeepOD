import argparse
import json
import uuid
import os


def lat_lon_from_geojson_or_json(entry):
    lat = entry.get('latitude', None)
    lon = entry.get('longitude', None)
    if lat is None and lon is None:
        try:
            coordinates = entry['geometry']['coordinates']
            lat = coordinates[1]
            lon = coordinates[0]
        except KeyError:
            pass
    return dict(latitude=lat, longitude=lon)


def convert_csv(json_data, name, ext='csv'):
    def build_element(crosswalk):
        return str(crosswalk['latitude']) + ',' + str(crosswalk[
                                                          'longitude']) + os.linesep

    elements = [build_element(lat_lon_from_geojson_or_json(crosswalk))
                for crosswalk in json_data.get('crosswalks', json_data.get(
                'features', []))]
    value = 'latitude,longitude' + os.linesep + ''.join(elements)
    output_filename = '.'.join([name, ext])
    with open(output_filename, 'w') as f:
        f.write(value)


def convert_maproulette(json_data, name, ext='tasks.json'):
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

    elements = [build_element(lat_lon_from_geojson_or_json(crosswalk))
                for crosswalk in json_data.get('crosswalks', json_data.get(
                'features', []))]
    value = str(elements).replace("'", '"')
    output_filename = '.'.join([name, ext])
    with open(output_filename, 'w') as f:
        f.write(value)


def convert_geojson(json_data, name, ext='geo.json'):
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
    outer['features'] = [build_element(lat_lon_from_geojson_or_json(crosswalk))
                         for crosswalk in json_data.get(
                'crosswalks', json_data.get('features', []))]
    value = str(outer).replace("'", '"')
    output_filename = '.'.join([name, ext])
    with open(output_filename, 'w') as f:
        f.write(value)


def convert(args):
    data = json.load(args.input_file)
    conv_kw = {}
    if args.outputfile is not None:
        file_args = args.outputfile.split('.')
        conv_kw['name'] = file_args[0]
        if len(file_args) > 1:
            conv_kw['ext'] = '.'.join(file_args[1:])
    else:
        file_args = args.input_file.name.split('.')
        conv_kw['name'] = file_args[0]
        # do not supply extension to use defaults
    for conv_func in args.conversion_funcs:
        conv_func(data, **conv_kw)


def mainfunc():
    parser = argparse.ArgumentParser(
            description='Convert crosswalks json to other formats', )
    parser.add_argument(
            '--csv',
            action='append_const',
            dest='conversion_funcs',
            const=convert_csv,
            help='convert to csv format with two columns [latitude,longitude], extension .csv')
    parser.add_argument('--geojson',
                        action='append_const',
                        dest='conversion_funcs',
                        const=convert_geojson,
                        help='convert to geojson format, extension .geo.json')
    parser.add_argument(
            '--maproulette',
            action='append_const',
            dest='conversion_funcs',
            const=convert_maproulette,
            help='convert to maproulette.org challenge format, extension .tasks.json')
    parser.add_argument(
            '--outputfile',
            action='store',
            dest='outputfile',
            default=None,
            help='explicit output filename if input filename is not wanted as name part. extension if present will be used instead of defaults')
    parser.add_argument('input_file',
                        type=argparse.FileType('r'),
                        help='name of crosswalks json file')
    parser.set_defaults(func=convert)

    args = parser.parse_args()
    if args.conversion_funcs is not None:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    mainfunc()
