#!/usr/bin/python
import getopt
import sys

from scores import *


def main(argv):
    inputfile = ''
    frames = 150
    try:
        opts, args = getopt.getopt(argv, "hi:f:", ["ifile=", "frames="])
    except getopt.GetoptError:
        print('main.py -i <inputfile> -f <frames=150>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <inputfile> -f <frames=150>')
            sys.exit()
        if opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-f", "--frames"):
            frames = arg
    print(f'Input file: {inputfile}; frames: {frames}')
    if inputfile == '':
        print('main.py -i <inputfile> -f <frames=150>')
        sys.exit(2)
    tests(inputfile, frames)


if __name__ == "__main__":
    main(sys.argv[1:])
