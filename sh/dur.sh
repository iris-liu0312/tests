#!/bin/bash
echo "=========="
echo "Duration of $1"
ffmpeg -i $1 2>&1 | grep Duration | cut -d ' ' -f 4 | sed s/,//
echo "=========="
