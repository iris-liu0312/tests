#!/usr/bin/python
import concurrent.futures
import csv
import getopt
import os
import sys

import scores
import cleanup
import estimateniqe


def parallel(f, files, frames, path):
    data = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        pool = executor.map(f, files, [frames] * len(files), [path] * len(files))
        res = []
        for i in pool:
            res.append(i)
        for i in range(0, len(files)):
            row = [files[i], frames, path, res[i][0], res[i][1]]
            data.append(row)
    return data


def main(argv):
    h = """main.py
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
    """
    # obtain arguments
    input_file = ''
    frames = 15
    path = ''
    t = 0
    try:
        opts, args = getopt.getopt(argv, "hi:f:d:t:", ["help", "inputfile=", "frames=",
                                                       "directory=", "train="])
    except getopt.GetoptError:
        print(h)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(h)
            sys.exit()
        if opt in ("-i", "--inputfile"):
            input_file = arg
        elif opt in ("-f", "--frames"):
            frames = arg
        elif opt in ("-d", "--directory"):
            path = arg
        elif opt in ("-t", "--train"):
            t = arg

    # only train model
    if t:
        estimateniqe.estimate_model_param(input_file)
        return 2  # train exit code

    # calculate in bulk
    if os.path.isdir(input_file):
        print("finding files")
        # find files
        mp4 = []
        ts = []
        for file in os.listdir(input_file):
            if file.endswith(".mp4"):
                mp4.append(os.path.join(input_file, file))
            elif file.endswith(".ts"):
                ts.append(os.path.join(input_file, file))
        mp4 = sorted(mp4)
        ts = sorted(ts)

        # run default NIQE in parallel
        print("running default NIQE")
        header = ['input file', 'frames', 'path', 'NIQE', 'time']
        mp4_d = parallel(scores.test, mp4, frames, '')
        ts_d = parallel(scores.test, ts, frames, '')
        with open('default.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(mp4_d)
            writer.writerows(ts_d)

        # run fitted NIQE in parallel
        print("running fitted NIQE")
        if path == '':
            path = 'niqe_fitted_parameters.mat'
        mp4_f = parallel(scores.test, mp4, frames, path)
        ts_f = parallel(scores.test, ts, frames, path)
        with open('fit.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(mp4_f)
            writer.writerows(ts_f)

        print("cleaning up")
        cleanup.clean()

        # remove default and fit
        os.remove('default.csv')
        os.remove('fit.csv')
        print("done")
        return 1  # automate calculation exit code

    # calculate single file
    if input_file == '':
        print(h)
        sys.exit(2)
    res = scores.test(input_file, frames, path)
    print('input file,frames,path,NIQE,time\n',
          f'{os.path.basename(os.path.normpath(input_file))},{frames},'
          f'{os.path.basename(os.path.normpath(path))},{res[0]},{res[1]}', end='')


if __name__ == "__main__":
    main(sys.argv[1:])
