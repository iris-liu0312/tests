#!/bin/python
import getopt
import os
import re
import sys
import urllib.request
from xml.dom import minidom

import main


def dash_read(argv):
    h = """dash_read.py
    Reads DASH manifest and goes into the highest quality playlist.
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
    manifest = minidom.parse(urllib.request.urlopen(url))
    adaptation = manifest.getElementsByTagName('AdaptationSet')[0]
    # segment template
    rep = adaptation.getElementsByTagName('Representation')[0]
    template = rep.getElementsByTagName('SegmentTemplate')[0]
    media = template.attributes['media'].value
    time = int(template.getElementsByTagName('S')[0].attributes['t'].value)+360360
    # obtain media name
    media = re.sub('\$.*\$', str(time), media)
    print(media)
    m4s = home + media

    destination = os.getcwd() + '/' + 'dash.mp4'
    urllib.request.urlretrieve(m4s, destination)
    main.main(["-i", destination, "-s", "1280x720"])


if __name__ == "__main__":
    dash_read(sys.argv[1:])
