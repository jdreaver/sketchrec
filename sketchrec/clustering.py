"""
This module holds all of the functions related to hierarchical clustering
of templates.
"""

import numpy as np
from sketchrec.image_template import stack_distance_maps

def distance_matrix_1(items, distance_fn):
    N = len(items)
    distances = np.zeros((N,N))
    for i in range(N):
        for j in range(i + 1, N):
            d = distance_fn(items[i], items[j])
            distances[i,j] = distances[j,i] = d
    return distances

def distance_matrix_3(items, distance_fn):
    N = len(items)
    distances = np.zeros((N, N))
    for i in range(N):
        row = np.array(([0]*(i+1) + [distance_fn(items[i], items[j])
                                     for j in range(i+1, N)]))
        distances[i] += row
    return distances + distances.T - np.diag(distances)

