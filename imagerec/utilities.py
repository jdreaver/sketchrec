"""
Contains extra functions for any other file. For now, jsut has
bounding boxes.
"""


import numpy as np
from itertools import tee, izip


# Bounding Boxes

def bounding_box(points):
    min_x, min_y = np.min(points, axis=0)
    max_x, max_y = np.max(points, axis=0)
    return np.array([(min_x, min_y), (max_x, min_y), 
                     (max_x, max_y), (min_x, max_y)])

def box_height(box):
    return box[2,1] - box[0,1]

def box_width(box):
    return box[1,0] - box[0,0]

def box_x(box):
    return box[0,0]

def box_y(box):
    return box[0,1]

def box_diagonal(box):
    return np.linalg.norm(box[0] - box[3])

def combine_boxes(boxes):
    """ Founds the bounding box for a set of bounding boxes."""
    (min_x, min_y) = np.min(boxes, axis=0)[0]
    (max_x, max_y) = np.max(boxes, axis=0)[0]
    return np.array([(min_x, min_y), (max_x, min_y), 
                     (max_x, max_y), (min_x, max_y)])

## def pairwise(iterable):
##     "s -> (s0,s1), (s1,s2), (s2, s3), ..."
##     a, b = tee(iterable)
##     next(b, None)
##     return izip(a, b)
