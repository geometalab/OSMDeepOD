if __name__ == "__main__":
    import sys, os
    from src.base.Bbox import Bbox
    from src.role.JobWorker import JobWorker
    from src.role.Manager import Manager
    from src.role.ResultWorker import ResultWorker

    def Usage(s = ""):
        print "Usage: main.py -role 'manager' left bottom right top |'jobworker' | 'resultworker' "
        print
        if s:
            print s
            print
        print "OSM-Crosswalk-Detection is a tool to extract the position of crosswalks on orthophotos."
        sys.exit(1)

    def _get_float(argv , i):
        try:
            return (float(argv[i]), (i + 1))
        except TypeError:
            Usage("ERROR: All boundingbox parameters needs to be floats")

    bottom, left, top, right = None, None, None, None
    argv = sys.argv
    if len(argv) < 3:
        Usage("ERROR: You have to specify all needed arguments.")
    i = 1
    role = ''
    if argv[i] == '-role':
        i += 1
        role = argv[i]

    if role == 'manager':
        if len(argv) < 7:
            Usage("ERROR: You have to specify the whole boundingbox.")
        left, i = _get_float(argv[i], i)
        bottom, i = _get_float(argv[i], i)
        right, i = _get_float(argv[i], i)
        top, i = _get_float(argv[i], i)

        if left is None or bottom is None or right is None or top is None:
            Usage("ERROR: You have to specify left, bottom, right and top .")
        if top < bottom:
            Usage("ERROR: 'top' must be bigger then 'bottom'")
        if right < left:
            Usage("ERROR: 'right' must be bigger then 'left'")
        big_bbox = Bbox(left, bottom, right, top)
        print 'Manger is running!'
        #Manager(big_bbox)
        print 'Manger is finished!'
    elif role == 'jobworker':
        print 'JobWorker is running!'
        #JobWorker()
    elif role == 'resultworker':
        print 'ResultWorker is running!'
        #ResultWorker()
    else:
        Usage("ERROR: Sorry, given role is not implemented yet.")


