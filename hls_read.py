#!/bin/python
import getopt
import sys


def main(argv):
    h = """hls_read.py
    Reads HLS manifest and obtains the video segment of the final item on the playlist.
    Only takes one argument, the URL to the HLS manifest.
    -h    help
    -i    url
    """
    # obtain arguments
    input_file = ''
    try:
        opts, args = getopt.getopt(argv, "hi:", ["help", "inputfile="])
    except getopt.GetoptError:
        print(h)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(h)
            sys.exit()
        if opt in ("-i", "--inputfile"):
            input_file = arg

    # exit with help
    if input_file == '':
        print(h)
        sys.exit(2)

    return -1


if __name__ == "__main__":
    main(sys.argv[1:])
