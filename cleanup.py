import csv
from datetime import date

import numpy as np
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
    for i in range(0, default.shape[0], 2):
        row = [-1] * 5  # time, TS-d, TS-f, MP4-d, MP4-f
        row[0] = re.sub(r'.*_|\..*$', '', default[i][0])
        row[1] = default[i + 1][3]
        row[2] = fit[i + 1][3]
        row[3] = default[i][3]
        row[4] = fit[i][3]
        cleaned.append(row)

    name = date.today().strftime("%m%d") + ".csv"
    with open(name, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['time', 'TS-d', 'TS-f', 'MP4-d', 'MP4-f'])
        writer.writerows(cleaned)
