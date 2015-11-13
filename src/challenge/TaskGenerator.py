if __name__ == "__main__":
    import sys, os
    import json
    import uuid

    def Usage(s = ""):
        print "Usage: TaskGenerator.py crosswalks.json"
        print
        if s:
            print s
            print
        print "TaskGenerator is a script to convert crosswalks.json to tasks.json in geojson format."
        sys.exit(1)

    def build_task(crosswalk):

        task = \
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
                                crosswalk.longitude,
                                crosswalk.longitude
                            ]
                        }
                    }
                ]
            },
            "identifier": str(uuid.uuid4()),
            "instruction": "Is this a crosswalk?"
        }
        return task

    argv = sys.argv
    if len(argv) < 2:
        Usage("ERROR: You have to specify all needed arguments.")

    file = argv[1]

    if not os.path.exists(file):
        Usage("ERROR: File does not exist.")

    with open(file, 'r') as f:
        data = json.load(f)

    tasks = []
    for crosswalk in data['crosswalks']:
        tasks.append(build_task(crosswalk))

    print tasks

    with open('tasks.json', 'w') as f:
        f.write(str(tasks))
