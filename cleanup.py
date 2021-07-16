import csv

import numpy as np
import re


def clean(default, fit, input_file):
    """
    Rearranges data into a csv file

    :param default: default NIQE calculations array
    :param fit: fitted NIQE calculations array
    :param input_file: file directory
    """
    # sort with timestamp
    default = np.array(default)
    fit = np.array(fit)
    default = default[np.argsort(default[:, 0])]
    fit = fit[np.argsort(fit[:, 0])]

    # compose array with NIQE scores
    data = []
    for i in range(0, default.shape[0], 2):
        row = [-1] * 5  # time, TS-d, TS-f, MP4-d, MP4-f
        row[0] = re.sub(r'.*_|\..*$', '', default[i][0])
        # ts data
        row[1] = default[i + 1][3]
        row[2] = fit[i + 1][3]
        # mp4 data
        row[3] = default[i][3]
        row[4] = fit[i][3]
        data.append(row)

    # write to file
    name = f"{input_file}.csv"
    with open(name, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['time', 'TS-d', 'TS-f', 'MP4-d', 'MP4-f'])
        writer.writerows(data)
