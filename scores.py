import time

import numpy as np
import skvideo.io
import skvideo.measure


def test():
    times = [time.time()]
    inputdata = skvideo.io.vread("./videos/8_min_480.mp4", num_frames=15, outputdict={"-pix_fmt": "gray"})[:, :, :, 0]
    print("loading finished. calculating viideo.")
    times.append(time.time())

    # test score
    viideo = skvideo.measure.viideo_score(inputdata)
    print("viideo finished. calculating niqe.")
    times.append(time.time())

    niqe = np.mean(skvideo.measure.niqe(inputdata))
    print("niqe finished.")
    times.append(time.time())

    print(f"=============================================\n"
          f"Total time: {time.time() - times[0]}s\n"
          f"NIQE: {niqe}, {times[-1] - times[-2]}s\n"
          f"VIIDEO: {viideo}, {times[-2] - times[-3]}s\n"
          f"frames: {inputdata.shape[0]}\n"
          f"=============================================")


def tests(video, frames):
    times = [time.time()]
    inputdata = skvideo.io.vread(video, num_frames=frames, outputdict={"-pix_fmt": "gray"})[:, :, :, 0]
    print("loading finished. calculating viideo.")
    times.append(time.time())

    # test score
    viideo = skvideo.measure.viideo_score(inputdata)
    print("viideo finished. calculating niqe.")
    times.append(time.time())

    niqe = np.mean(skvideo.measure.niqe(inputdata))
    print("niqe finished.")
    times.append(time.time())

    print(f"=============================================\n"
          f"Total time: {time.time() - times[0]}s\n"
          f"NIQE: {niqe}, {times[-1] - times[-2]}s\n"
          f"VIIDEO: {viideo}, {times[-2] - times[-3]}s\n"
          f"frames: {inputdata.shape[0]}\n"
          f"=============================================")
