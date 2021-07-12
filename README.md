# tests
## Usage
Call `main.py` with the necessary commands:
```
main.py
Input the video you want to calculate NIQE for.
If no directory for training or mat file is specified,
the default NIQE is used.
Directory calculation assumes niqe_fitted_parameters.mat
is in the current directory if none are given
-h      help
-i      input video file/directory to be analyzed
    or directory to train NIQE model (add -t 1 option)

Optionals:
-f 150  frames to analyze, default 150
-d      parameters mat file for NIQE
-t 0    whether input is training directory, default 0 (false)
        if 1 (true), all other options are ignored
```

### Sample calls
- `python main.py -i video.mp4 -f 15`
- `python main.py -i video_directory (-d niqe.mat)`
- `python main.py -i train_directory -t 1`

## Issues
A current known issue is that the fitted NIQE score is much higher than default NIQE. This may be due to 2 things:
1. Training data was averaged to fit (36, 36) dimensions when calculating covariance
2. Default algorithm took out data points, although it was unclear why they did so
