import time

import numpy as np
import os
import skvideo.io
import skvideo.measure
import estimateniqe


def test(video, frames, t):
    viideo = -1
    niqe = -1
    times = [time.time()]
    inputdata = skvideo.io.vread(video, num_frames=frames, outputdict={"-pix_fmt": "gray"})[:, :, :, 0]
    times.append(time.time())

    # test score
    if "v" in t:
        viideo = skvideo.measure.viideo_score(inputdata)
        times.append(time.time())

    if "n" in t:
        niqe = np.mean(skvideo.measure.niqe(inputdata))
        times.append(time.time())

    print(f"NIQE, {round(niqe, 5)}, time, {round(times[-1] - times[-2])}\n" * ("n" in t),
          f"VIIDEO, {round(viideo, 5)}, time, {round(times[-2] - times[-3])}\n" * ("v" in t),
          f"Total time,  {round(time.time() - times[0])}\n" * ("n" in t) * ("v" in t))


def fit_test(video, frames, path, t):
    viideo = -1
    niqe = -1

    model = path
    if os.path.isdir(path):
        estimateniqe.estimate_model_param(path)
        model = 'niqe_fitted_parameters.mat'

    times = [time.time()]
    inputdata = skvideo.io.vread(video, num_frames=frames, outputdict={"-pix_fmt": "gray"})[:, :, :, 0]
    times.append(time.time())

    # test score
    if t in ("v", "V"):
        viideo = skvideo.measure.viideo_score(inputdata)
        times.append(time.time())

    if t in ("n", "N"):
        niqe = np.mean(estimateniqe.fit_niqe(inputdata, model))
        times.append(time.time())

    print(f"NIQE, {round(niqe, 5)}, time, {round(times[-1] - times[-2])}\n" * ("n" in t),
          f"VIIDEO, {round(viideo, 5)}, time, {round(times[-2] - times[-3])}\n" * ("v" in t),
          f"Total time,  {round(time.time() - times[0])}\n" * ("n" in t) * ("v" in t))
