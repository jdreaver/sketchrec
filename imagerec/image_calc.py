from scipy import ndimage
import numpy as np

def bounding_box(points):
    min_x, min_y = np.min(points, axis=0)
    max_x, max_y = np.max(points, axis=0)
    return np.array([(min_x, min_y), (max_x, min_y), 
                     (max_x, max_y), (min_x, max_y)])

def inflate_points(points, min_box_dim=48):
    bbox = bounding_box(points)
    width = bbox[1][0] - bbox[0][0]
    height = bbox[2][1] - bbox[1][1]
    moved = points - bbox[0]
    dim = min_box_dim - 1  # points must fit within 48x48 grid
    inflation = np.min([dim/width, dim/height])
    return np.array(map(lambda point: 
            np.dot(np.diag([inflation]*2), point), moved)).astype(int)

def distance_map(points, dim=48):
    centered = points - np.mean(points, axis=0) + np.array([24,24])
    inflated = inflate_points(centered, dim)
    grid = np.zeros([dim, dim])
    for point in inflated:
        grid[point[0]][point[1]] = 1
    dist_map = ndimage.morphology.distance_transform_edt(1 - grid)
    return (grid, dist_map, inflated.astype(int))
