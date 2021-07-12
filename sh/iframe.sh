#!/bin/bash
file_name="$(basename -s .ts $1)_"
ffmpeg -i $1 -f image2 -vf "select='eq(pict_type,PICT_TYPE_I)'" -vsync vfr $2/$file_name%03d.png
