import time

import numpy as np
import skvideo.io
import skvideo.measure
import estimateniqe


def test(video, frames, path):
    times = [time.time()]
    inputdata = skvideo.io.vread(video, num_frames=frames, outputdict={"-pix_fmt": "gray"})[:, :, :, 0]
    times.append(time.time())

    # test score
    if path != '':
        niqe = float(np.mean(estimateniqe.fit_niqe(inputdata, path)))
    else:
        niqe = float(np.mean(skvideo.measure.niqe(inputdata)))
    times.append(time.time())

    return round(niqe, 5), round(times[-1] - times[-2])
