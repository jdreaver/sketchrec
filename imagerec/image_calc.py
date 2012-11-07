import scipy
from scipy import ndimage
import numpy as np

def bounding_box(iterable):
    min_x, min_y = np.min(iterable, axis=0)
    max_x, max_y = np.max(iterable, axis=0)
    return np.array([(min_x, min_y), (max_x, min_y), 
                     (max_x, max_y), (min_x, max_y)])

def inflate_points(points, min_box_dim=48):
    bb = bounding_box(points)
    width = bb[1][0] - bb[0][0]
    height = bb[2][1] - bb[1][1]
    inflation = np.min([min_box_dim/width, min_box_dim/height])
    return np.array(map(lambda point: 
            np.dot(np.diag([inflation]*2), point), points)).astype(int)

def distance_map(points, dim=48):
    centered = points - np.mean(points, axis=0)
    inflated = inflate_points(centered, dim)
    grid = np.zeros([10,10])
    for point in inflated:
        grid[point[0]][point[1]] = 1
    dist_map = ndimage.morphology.distance_transform_edt(1 - grid)
    return (grid, dist_map)
