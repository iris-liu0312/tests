#!/bin/bash
# coding = utf-8
score="/Users/P3039312/PycharmProjects/tests/main.py"
niqe='/Users/P3039312/PycharmProjects/tests/niqe_fitted_parameters.mat'
cleanup='/Users/P3039312/PycharmProjects/tests/cleanup.py'

# Calculate default NIQE
echo 'calculating default NIQE for mp4 files...'
for mp4_file in $1/*.mp4
do
	py $score -i $mp4_file >> default.csv &
done
wait
echo 'calculating default NIQE for ts files...'
for ts_file in $1/*.ts
do
	py $score -i $ts_file >> default.csv &
done
wait

# Calculate fitted NIQE
echo 'calculating fitted NIQE for mp4 files...'
for mp4_file in $1/*.mp4
do
	py $score -i $mp4_file -d $niqe >> fit.csv &
done
wait
echo 'calculating fitted NIQE for ts files...'
for ts_file in $1/*.ts
do
	py $score -i $ts_file -d $niqe >> fit.csv &
done
wait

# clean up data
echo 'cleaning up'
py $cleanup
wait
rm default.csv
rm fit.csv

# extract i-frames
# echo "extracting i-frames from today's ts files..."
# for ts_file in $1/*.ts
# do
# 	bash sh/iframe.sh $ts_file ny1/ts_iframes &
# done

# train with dummy file as input to just train new model
# time py tests/main.py -d ny1/ts_iframes/ -i dummy.ts