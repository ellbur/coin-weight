
from __future__ import division, print_function
from pylab import *
import multiprocessing

phi = (1 + sqrt(5)) / 2

N = 20
block_1 = array([
    n_1
    for n_1 in range(N)
    for n_2 in range(N)
    for n_3 in range(N)
])

block_2 = array([
    n_2
    for n_1 in range(N)
    for n_2 in range(N)
    for n_3 in range(N)
])

block_3 = array([
    n_3
    for n_1 in range(N)
    for n_2 in range(N)
    for n_3 in range(N)
])

def score_for_ratios(ratio_1, ratio_2):
    weight_1 = 1.0
    weight_2 = weight_1 * ratio_1
    weight_3 = weight_1 * ratio_2

    weights = block_1 * weight_1 + block_2 * weight_2 + block_3 * weight_3
    weights = array(list(sorted(weights)))
    
    middle_weights = weights[N*3:-N*3]
    dmw = diff(middle_weights)
    score = std(dmw) / mean(dmw)
    
    return score

ratio_1s = linspace(1, 2, 500)
ratio_2s = linspace(1, 2, 500)

Ratio_1s, Ratio_2s = meshgrid(ratio_1s, ratio_2s)
Scores = zeros(Ratio_1s.shape)

def calc_block(i1, i2, j1, j2):
    result = zeros((i2-i1, j2-j1))
    for i in range(i1, i2):
        for j in range(j1, j2):
            ratio_1 = Ratio_1s[i, j]
            ratio_2 = Ratio_2s[i, j]
            score = score_for_ratios(ratio_1, ratio_2)
            result[i-i1, j-j1] = score
    return result

def calc(b):
    i1, i2, j1, j2 = b
    return calc_block(i1, i2, j1, j2)

step_size = 20

blocks = [ ]

for i in range(0, Ratio_1s.shape[0], step_size):
    for j in range(0, Ratio_1s.shape[1], step_size):
        i1 = i
        i2 = min(i + step_size, Ratio_1s.shape[0])
        j1 = j
        j2 = min(j + step_size, Ratio_1s.shape[1])
        blocks.append((i1, i2, j1, j2))
    
pool = multiprocessing.Pool(multiprocessing.cpu_count())
results = pool.map(calc, blocks)

Scores = zeros(Ratio_1s.shape)
for block, result in zip(blocks, results):
    i1, i2, j1, j2 = block
    Scores[i1:i2, j1:j2] = result

imsave('scores.png', 1.0/Scores)

