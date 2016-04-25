if __name__ == "__main__":
    import sys
    from src.base.Bbox import Bbox
    from src.role.Worker import Worker
    from src.role.Manager import Manager
    from redis import Redis

    def Usage(s = ""):
        print "Usage: main.py --redis REDIS_IP_ADDR --role 'manager' left bottom right top |'jobworker' | 'resultworker' "
        print
        if s:
            print s
            print
        print "OSM-Crosswalk-Detection is a tool to extract the position of crosswalks on orthophotos."
        sys.exit(1)

    def _get_float(arg):
        try:
            return float(arg)
        except ValueError:
            Usage("ERROR: All boundingbox parameters needs to be floats")

    bottom, left, top, right = None, None, None, None
    argv = sys.argv
    if len(argv) < 5:
        Usage("ERROR: You have to specify all needed arguments.")
    i = 1
    redis_ip = ''
    if argv[i] == '--redis':
        i += 1
        redis_ip = argv[i]
        redis = [str(redis_ip), '40001', 'crosswalks']
        i += 1

    role = ''
    if argv[i] == '--role':
        i += 1
        role = argv[i]
        i += 1

    if role == 'manager':
        if len(argv) < 7:
            Usage("ERROR: You have to specify the whole boundingbox.")
        left = _get_float(argv[i])
        i += 1
        bottom = _get_float(argv[i])
        i += 1
        right = _get_float(argv[i])
        i += 1
        top = _get_float(argv[i])

        if left is None or bottom is None or right is None or top is None:
            Usage("ERROR: You have to specify left, bottom, right and top .")
        if top < bottom:
            Usage("ERROR: 'top' must be bigger then 'bottom'")
        if right < left:
            Usage("ERROR: 'right' must be bigger then 'left'")
        big_bbox = Bbox.from_lbrt(left, bottom, right, top)
        print 'Manger is running!'
        Manager.from_big_bbox(big_bbox, redis)
        print 'Manger is finished!'
    elif role == 'jobworker':
        print 'JobWorker is running!'
        jobWorker = Worker.from_worker(['jobs'])
        jobWorker.run(redis)
    elif role == 'resultworker':
        print 'ResultWorker is running!'
        resultWorker = Worker.from_worker(['results'])
        resultWorker.run(redis)
    else:
        Usage("ERROR: Sorry, given role is not implemented yet.")



