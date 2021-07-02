import time

import numpy as np
import os
import skvideo.io
import skvideo.measure
import estimateniqe


def test(video, frames, t):
    times = [time.time()]
    print(f"* Load {video} -----")
    inputdata = skvideo.io.vread(video, num_frames=frames, outputdict={"-pix_fmt": "gray"})[:, :, :, 0]
    times.append(time.time())

    # test score
    if "v" in t:
        print("* Calculate VIIDEO -----")
        viideo = skvideo.measure.viideo_score(inputdata)
        times.append(time.time())

    if "n" in t:
        print("* Calculate NIQE -----")
        niqe = np.mean(skvideo.measure.niqe(inputdata))
        times.append(time.time())

    print(f"---------------------------------------------\n",
          f"NIQE:   {niqe} | {times[-1] - times[-2]}s\n"*("n" in t),
          f"VIIDEO: {viideo} | {times[-2] - times[-3]}s\n"*("v" in t),
          f"Total:  {time.time() - times[0]}s\n",
          f"frames: {inputdata.shape[0]}\n"
          f"---------------------------------------------")


def fit_test(video, frames, path, t):
    model = path
    if os.path.isdir(path):
        estimateniqe.estimate_model_param(path)
        model = 'niqe_fitted_parameters.mat'

    times = [time.time()]
    print(f"* Load {video} -----")
    inputdata = skvideo.io.vread(video, num_frames=frames, outputdict={"-pix_fmt": "gray"})[:, :, :, 0]
    times.append(time.time())

    # test score
    if "v" in t:
        print("* Calculate VIIDEO -----")
        viideo = skvideo.measure.viideo_score(inputdata)
        times.append(time.time())

    if "n" in t:
        print("* Calculate NIQE -----")
        niqe = np.mean(estimateniqe.fit_niqe(inputdata, model))
        times.append(time.time())

    print(f"---------------------------------------------\n",
          f"NIQE:   {niqe} | {times[-1] - times[-2]}s\n"*("n" in t),
          f"VIIDEO: {viideo} | {times[-2] - times[-3]}s\n"*("v" in t),
          f"Total:  {time.time() - times[0]}s\n",
          f"frames: {inputdata.shape[0]}\n"
          f"---------------------------------------------")