""" 
This file contains the definition for an ImageTemplate as well as
all of the functions for creating an image template and finding
the distance between two templates.
"""

import numpy as np
from scipy import ndimage
from template import Template
from utilities import bounding_box, box_width, box_height

class ImageTemplate(Template):
    """
    An image template contains a rasterized set of the template's
    strokes, and the distance transform computed from said rasterized
    points. The distance map and rsaterized corrdinates are flattened
    to we can more easily compute the hausdorff distance between two
    templates.
    """
    
    def __init__(self, strokes, name="NO LABEL", timestamps = None, dim=48):
        points = np.array([point  for stroke in strokes for point in stroke])
        (grid, dmap, r_points) = distance_map(points, dim)
        self.grid = grid
        self.distance_map = dmap
        self.rasterized_points = r_points
        self.dimension = dim
        # Following used for hausdorff distance
        self.flat_map = dmap.flatten()
        self.flat_points = np.array([dim*p[0] + p[1] for p in r_points])
        self.num_r_points = len(r_points)
        self.map_dict = dict(zip(range(dim*dim), self.flat_map))
        super(ImageTemplate, self).__init__(strokes, name, timestamps)


def convert_to_image(template, dim = 48):
    """ Converts a standard template to an image template."""
    return ImageTemplate(template.strokes, template.name, 
                         template.timestamps, dim)

def multiple_to_image(templates, dim = 48):
    """ Combines the strokes and timestamps of multiple templates into
    a single image template. Assumes each stroke has the same name."""
    return ImageTemplate([stroke for t in templates for stroke in t.strokes],
                         templates[0].name, 
                         [stamp for t in templates for stamp
                          in t.timestamps],
                         dim)

# ImageTemplate initialization functions.

def inflate_points(points, min_box_dim=48):
    """
    Takes a set of raw stroke points and scales them to a (default)
    48x48 grid. The points are scaled with the aspect ratio intact.
    """
    bbox = bounding_box(points)
    width = box_width(bbox)
    height = box_height(bbox)
    moved = points - bbox[0]
    dim = min_box_dim - 1  # points must fit within 48x48 grid
    inflation = 1/np.max([width/dim, height/dim]) # 1/" prevents DivideByZero
    return np.array(map(lambda point: 
            np.dot(np.diag([inflation]*2), point), moved)).astype(int)

def distance_map(points, dim=48):
    """
    Given a binary grid of points, we compute the distance map. Any
    point on the distance map encodes that point's distance to the
    nearest rsaterized point.
    """
    if len(points) == 1: 
        inflated = np.array(([dim/2, dim/2],))
    else:
        centered = points - np.mean(points, axis=0) + np.array([24, 24])
        inflated = inflate_points(centered, dim)
    grid = np.zeros([dim, dim])
    for point in inflated:
        grid[point[0], point[1]] = 1
    dist_map = ndimage.morphology.distance_transform_edt(1 - grid)
    return (grid, dist_map, inflated.astype(int))
        
# Distance functions

def list_classification_old(unknown, training):
    """ 
    Finds the closest training template to the unkown using the
    modified hausdorff distance.
    """
    min_dist = (1.0, 'ERROR')
    for temp in training:
        dis = np.zeros(2)
        dis[0] = np.sum(unknown.flat_map.take(temp.flat_points))/temp.num_r_points
        dis[1] = np.sum(temp.flat_map.take(unknown.flat_points))/unknown.num_r_points
        dist = max(dis[0], dis[1])/(1.4142 * unknown.dimension)
        min_dist = min([min_dist, (dist, temp.name)])
    return min_dist[1]

def list_classification(unknown, training):
    """ 
    Finds the closest training template to the unkown using the
    modified hausdorff distance.
    """
    min_dist = (1.0, 'ERROR')
    for temp in training:
        dist = max(
            np.sum(unknown.flat_map.take(temp.flat_points))/temp.num_r_points,
            np.sum(temp.flat_map.take(unknown.flat_points))/unknown.num_r_points)
        min_dist = min([min_dist, (dist, temp.name)])
    min_dist = (min_dist[0] / (1.4142 * unknown.dimension), min_dist[1])
    return min_dist[1]

# def old_mod_hauss_distance(imageA, imageB):
#     assert imageA.dimension == imageB.dimension

#     directed_distances = [0.0, 0.0]
#     for i, (temp1, temp2) in enumerate([(imageA, imageB), (imageB, imageA)]):
#         d_sum = 0.0
#         for p in temp1.rasterized_points:
#             d_sum += temp2.distance_map[p[0], p[1]]
#         directed_distances[i] = d_sum/len(temp1.rasterized_points)
    
#     return np.max(directed_distances) / (np.sqrt(2) * imageA.dimension)
    
def mod_hauss_distance(imageA, imageB):
    d1 = np.sum(imageA.flat_map.take(imageB.flat_points))/imageB.num_r_points     
    d2 = np.sum(imageB.flat_map.take(imageA.flat_points))/imageA.num_r_points
    return np.max([d1, d2])/(1.4142 * imageA.dimension)

# def old_list_classification(unknown, training):
#     distances = [(mod_hauss_distance(unknown, t), t.name) 
#                  for t in training]
#     return min(distances)[1]



    
