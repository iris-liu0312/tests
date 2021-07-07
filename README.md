# tests
Sample call: `python tests/main.py -i video.mp4 -d mat_file_or_training_directory`

## Usage
Call `main.py` with the necessary commands:
```
Input the video you want to analyze as well as some other options.
If no directory for training is specified, the default NIQE is used.
-h      help
-i      input video file to be analyzed 

Optionals:
-f      frames to analyze, default 150
-t [n] specifies the metrics to calculate. default n
        v = VIIDEO
        n = NIQE
-d      directory for image database to train NIQE
        or parameters mat file for NIQE
```

A current known issue is that the fitted NIQE score is much higher than default NIQE. This may be due to 2 things:
1. Training data was averaged to fit (36, 36) dimensions when calculating covariance
2. Default algorithm took out data points, although it was unclear why they did so
