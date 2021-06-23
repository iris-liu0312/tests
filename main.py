#!/usr/bin/python
import getopt
import sys

from scores import *


def main(argv):
    inputfile = ''
    frames = 15
    try:
        opts, args = getopt.getopt(argv, "hi:f:", ["ifile=", "frames="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -f <frames=15>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -f <frames=15>')
            sys.exit()
        if opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-f", "--frames"):
            frames = arg
    print(f'Input file: {inputfile}')
    tests(inputfile, frames)


if __name__ == "__main__":
    main(sys.argv[1:])
