import csv
import numpy as np
import os
import re


def clean():
    default = []
    fit = []
    with open('default.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[0] != 'input file':
                default.append(row)

    with open('fit.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[0] != 'input file':
                fit.append(row)
    # strip whitespace and sort with timestamp
    default = np.char.strip(default)
    default = default[np.argsort(default[:, 0])]
    fit = np.char.strip(fit)
    fit = fit[np.argsort(fit[:, 0])]

    # clean
    cleaned = []
    row = ['a', -1, -1, -1, -1]  # time, TS-d, TS-f, MP4-d, MP4-f
    for i in range(0, default.shape[0]):
        niqe_d = default[i]
        niqe_f = fit[i]
        if row[0] == -1:
            row[0] = re.sub(r'.*_|\..*$', '', niqe_d[0])
        # ts files
        if i % 2 == 0:
            row[1] = niqe_d[3]
            row[2] = niqe_f[3]
        else:
            row[3] = niqe_d[3]
            row[4] = niqe_f[3]
        cleaned.append(row)

    with open('cleaned.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['time', 'TS-d', 'TS-f', 'MP4-d', 'MP4-f'])
        writer.writerows(cleaned)
