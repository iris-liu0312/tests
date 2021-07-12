#!/usr/bin/python
import getopt
import sys
import os

from scores import *


def main(argv):
    h = """main.py
    Input the video you want to calculate NIQE for.
    If no directory for training or mat file is specified,
    the default NIQE is used.
    -h      help
    -i      input video file to be analyzed 
    
    Optionals:
    -f      frames to analyze, default 150
    -d      directory for image database to train NIQE
            or parameters mat file for NIQE
    """
    input_file = ''
    frames = 150
    path = ''
    try:
        opts, args = getopt.getopt(argv, "hi:f:d:m:", ["help", "inputfile=", "frames=",
                                                       "directory="])
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
    print(f'input file, {os.path.basename(os.path.normpath(input_file))}\n',
          f'frames, {frames}\n',
          f'path, {os.path.basename(os.path.normpath(path))}')
    if input_file == '':
        print(h)
        sys.exit(2)
    if path:
        fit_test(input_file, frames, path)
    else:
        test(input_file, frames)


if __name__ == "__main__":
    main(sys.argv[1:])
