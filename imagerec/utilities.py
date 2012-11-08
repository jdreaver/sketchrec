import numpy as np
from itertools import tee, izip

def bounding_box(points):
    min_x, min_y = np.min(points, axis=0)
    max_x, max_y = np.max(points, axis=0)
    return np.array([(min_x, min_y), (max_x, min_y), 
                     (max_x, max_y), (min_x, max_y)])

def box_height(bounding_box):
    return bounding_box[2,1] - bounding_box[0,1]

def box_width(bounding_box):
    return bounding_box[1,0] - bounding_box[0,0]


def combine_boxes(boxes):
    """ Founds the bounding box for a set of bounding boxes."""
    (min_x, min_y) = np.min(boxes, axis=0)[0]
    (max_x, max_y) = np.max(boxes, axis=0)[0]
    return np.array([(min_x, min_y), (max_x, min_y), 
                     (max_x, max_y), (min_x, max_y)])

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)
