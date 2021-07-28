#!/bin/bash
# extract i-frames
echo 'extracting frames...'
for ts_file in $1/*.ts
do
  bash sh/iframe.sh $ts_file $2
done
wait
echo 'total files now:'
ls $2 | wc -l
# train
echo 'training...'
time python3 main.py -i $2 -t 1