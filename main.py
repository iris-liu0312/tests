#!/usr/bin/python
import getopt
import sys

from scores import *


def main(argv):
    h = """main.py
    Input the video you want to analyze as well as some other options.
    If no directory for training is specified, the default NIQE is used.
    -h      help
    -i      input video file to be analyzed 
    
    Optionals:
    -f      frames to analyze, default 150
    -t [n] specifies the metrics to calculate. default n
            v = VIIDEO
            n = NIQE
    -d      directory for image database to train NIQE
            or parameters mat file for NIQE
    """
    input_file = ''
    frames = 150
    t = 'n'
    path = ''
    try:
        opts, args = getopt.getopt(argv, "hi:f:d:m:t:", ["help", "inputfile=", "frames=",
                                                         "directory=", "tests="])
    except getopt.GetoptError:
        print(h)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(h)
            sys.exit()
        if opt in ("-i", "--inputfile"):
            input_file = arg
        elif opt in ("-f", "--frames"):
            frames = arg
        elif opt in ("-d", "--directory"):
            path = arg
        elif opt in ("-t", "--tests"):
            t = arg
    print(f'input file, {input_file}\n',
          f'frames, {frames}\n',
          f'tests, {t}')
    if not path == '':
        print(f'path, {path}')
    if input_file == '':
        print(h)
        sys.exit(2)
    if path:
        fit_test(input_file, frames, path, t)
    else:
        test(input_file, frames, t)


if __name__ == "__main__":
    main(sys.argv[1:])
