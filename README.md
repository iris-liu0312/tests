# tests
known issue: on the same file, default NIQE = 13, fitted NIQE = 67 even though supposedly the training database is the same.

- might have been due to 2 things, 1. data was averaged and shrunk to fit (36, 36) dimensions when calculating covariance, 2. default algorithm takes out data points
