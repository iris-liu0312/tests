#!/bin/python
import getopt
import os
import sys
import urllib.request

import main


def hls_read(argv):
    h = """hls_read.py
    Reads HLS manifest and goes into the highest quality playlist.
    Obtains last video segment available on the playlist.
    The video segment is saved to the current destination, and NIQE is calculated.
    -h    help
    -u    url
    """
    # obtain arguments
    url = ''
    try:
        opts, args = getopt.getopt(argv, "hu:", ["help", "url="])
    except getopt.GetoptError:
        print(h)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(h)
            sys.exit()
        if opt in ("-u", "--url"):
            url = arg

    # exit with help
    if url == '':
        print(h)
        sys.exit(2)

    # extract home-url
    home = url.replace(os.path.basename(url), '')
    manifest = urllib.request.urlopen(url)
    found = False
    for line in manifest:
        decoded_line = line.decode("utf-8")
        print(decoded_line)
        if found:
            manifest = home+decoded_line
            break
        if "STREAM-INF" in decoded_line:
            found = True
    # HTTPResponse object not reversible, will take some time to run through the whole file
    playlist = urllib.request.urlopen(manifest)
    decoded_line = ''
    for line in playlist:
        decoded_line = line.decode("utf-8")
        pass
    ts = home+decoded_line.rstrip()
    print(ts)
    destination = (os.getcwd()+'/'+decoded_line).replace("\r\n", '')
    urllib.request.urlretrieve(ts, destination)
    main.main(["-i", destination, "-s", '1280x720'])


if __name__ == "__main__":
    hls_read(sys.argv[1:])
