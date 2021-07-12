import time

import numpy as np
import os
import skvideo.io
import skvideo.measure
import estimateniqe


def test(video, frames):
    times = [time.time()]
    inputdata = skvideo.io.vread(video, num_frames=frames, outputdict={"-pix_fmt": "gray"})[:, :, :, 0]
    times.append(time.time())

    # test score
    niqe = np.mean(skvideo.measure.niqe(inputdata))
    times.append(time.time())

    print(f"{round(niqe, 5)},{round(times[-1] - times[-2])}")


def fit_test(video, frames, path):

    model = path
    if os.path.isdir(path):
        estimateniqe.estimate_model_param(path)
        model = 'niqe_fitted_parameters.mat'

    times = [time.time()]
    inputdata = skvideo.io.vread(video, num_frames=frames, outputdict={"-pix_fmt": "gray"})[:, :, :, 0]
    times.append(time.time())

    # test score
    niqe = np.mean(estimateniqe.fit_niqe(inputdata, model))
    times.append(time.time())

    print(f"{round(niqe, 5)},{round(times[-1] - times[-2])}")
