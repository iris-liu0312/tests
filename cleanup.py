import csv
import numpy as np


# need default and test
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
print(default)

# clean
cleaned = []
for i in range(0, default.shape[0], 2):
    row = [-1] * 5  # time, TS-d, TS-f, MP4-d, MP4-f
    if row[0] == -1:
        row[0] = default[i][0][5:13]
        row[1] = default[i+1][3]
        row[2] = fit[i+1][3]
        row[3] = default[i][3]
        row[4] = fit[i][3]
    cleaned.append(row)

with open('cleaned.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['time', 'TS-d', 'TS-f', 'MP4-d', 'MP4-f'])
    writer.writerows(cleaned)
