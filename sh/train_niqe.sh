#!/bin/bash
# extract i-frames
echo "extracting i-frames from today's ts files..."
for ts_file in $1/*.ts
do
  bash sh/iframe.sh $ts_file ny1/ts_iframes &
done
wait
# train with dummy file as input to just train new model
time py tests/main.py -d ny1/ts_iframes/ -i dummy.ts
