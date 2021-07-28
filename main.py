#!/usr/bin/python
import concurrent.futures
import getopt
import os
import sys

import scores
import cleanup
import estimateniqe


def parallel(files, frames, path):
    """
    Runs default and fitted NIQE model on multiple files in parallel

    :param files: array of file names
    :param frames: frames to analyze, default 60
    :param path: parameters mat file for NIQE
    :return: array of file names with mat file path and results
    """
    data = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        pool = executor.map(scores.test, files, [frames] * len(files), [path] * len(files))
        if path == '':
            path = 'default'
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
    -f 60  frames to analyze, default 60
    -d      parameters mat file for NIQE
    -t 0    whether input is training directory, default 0 (false)
            if 1 (true), all other options are ignored
    -v      verbose output, i.e. prints which step the program is on
    """
    # obtain arguments
    input_file = ''
    frames = 60
    path = ''
    t = 0
    v = 0
    try:
        opts, args = getopt.getopt(argv, "hi:f:d:t:v", ["help", "inputfile=", "frames=",
                                                        "directory=", "train=", "verbose"])
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
        elif opt in ("-v", "--verbose"):
            v = 1

    # exit with help
    if input_file == '':
        print(h)
        sys.exit(2)

    # only train model
    if t:
        estimateniqe.estimate_model_param(input_file)
        return 2  # train exit code

    # calculate in bulk
    if os.path.isdir(input_file):
        if v:
            print("finding files")
        mp4 = []
        ts = []
        for file in os.listdir(input_file):
            if file.endswith(".mp4"):
                mp4.append(os.path.join(input_file, file))
            elif file.endswith(".ts"):
                ts.append(os.path.join(input_file, file))
        mp4 = sorted(mp4)
        ts = sorted(ts)

        if v:
            print("running default NIQE")
        default = parallel(mp4, frames, '')
        default += parallel(ts, frames, '')

        if v:
            print("running fitted NIQE")
        if path == '':
            path = 'niqe_fitted_parameters.mat'
        fit = parallel(mp4, frames, path)
        fit += parallel(ts, frames, path)

        if v:
            print("cleaning up")
        cleanup.clean(default, fit, os.path.basename(os.path.normpath(input_file)))
        if v:
            print("done")
        return 1  # automate calculation exit code

    # calculate single file
    res = scores.test(input_file, frames, path)
    if path == '':
        path = 'default'
    print(f'input file | {os.path.basename(os.path.normpath(input_file))}\n',
          f'frames    | {frames}\n',
          f'path      | {os.path.basename(os.path.normpath(path))}\n',
          f'NIQE      | {res[0]}\n',
          f'time      | {res[1]}')
    if path == 'default':
        path = 'niqe_fitted_parameters.mat'
        res = scores.test(input_file, frames, path)
        print(f' path      | {os.path.basename(os.path.normpath(path))}\n',
              f'NIQE      | {res[0]}\n',
              f'time      | {res[1]}')


if __name__ == "__main__":
    main(sys.argv[1:])
