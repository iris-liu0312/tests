import time

import numpy as np
import skvideo.io
import skvideo.measure
import estimateniqe


def test(video, frames, path):
    """
    Calculates average NIQE for a video

    :param video: video to be analyzed
    :param frames: frames to analyze
    :param path: parameter mat file
    :return: NIQE score and calculation time
    """
    times = [time.time()]
    inputdata = skvideo.io.vread(video, num_frames=frames, as_grey=True)
    times.append(time.time())

    # test score
    if path != '':
        niqe = float(np.mean(estimateniqe.fit_niqe(inputdata, path)))
    else:
        niqe = float(np.mean(skvideo.measure.niqe(inputdata)))
    times.append(time.time())

    return round(niqe, 5), round(times[-1] - times[-2])
