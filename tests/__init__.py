import sys
import os
maindir = os.path.realpath(
    os.path.join(
        os.path.dirname(__file__),
        '../src'))
sys.path += [maindir]
