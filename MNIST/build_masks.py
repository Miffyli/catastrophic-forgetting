# -*- coding: utf-8 -*-

from sklearn.model_selection import StratifiedKFold
import numpy as np
import tensorflow as tf

NUM_FOLDS = 10
SEED = 15626  # generated by RANDOM.ORG

# load mnist
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

# build mask for folds
skf = StratifiedKFold(n_splits=NUM_FOLDS, shuffle=True, random_state=SEED)
folds = [i for _, i in skf.split(x_train, y_train)]

# build mask for each digit in folds
masks = [list() for _ in range(len(folds) + 1)]
assert(min(y_train) == 0)
for j in range(max(y_train) + 1):
    for i in range(len(folds)):
        assert(len(y_train.shape) == 1)
        mask = np.zeros(len(y_train), dtype=bool)
        mask[folds[i]] += y_train[folds[i]] == j
        masks[i].append(mask)
    masks[-1].append(y_test == j)
masks = np.array(masks)

# print report
print('fold,number,count')
lines = list()
for j in range(max(y_train) + 1):
    for i in range(len(folds)):
        lines.append('{},{},{}'.format(i, j, sum(masks[i, j])))
    lines.append('holdout,{},{}'.format(j, sum(masks[-1, j])))
for line in sorted(lines):
    print(line)

# save masks
np.save('masks.npy', masks)
