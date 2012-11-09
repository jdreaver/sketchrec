import numpy as np
from scipy import ndimage
from template import Template
from utilities import bounding_box, box_width, box_height

""" 
This file contains the definition for an ImageTemplate as well as
all of the functions for creating an image template and finding
the distance between two templates.
"""

class ImageTemplate(Template):
    """
    An image template contains a rasterized set of the template's
    strokes, and the distance transform computed from said rasterized points
    """
    
    def __init__(self, strokes, name="NO LABEL", timestamps = None, dim=48):
        points = np.array([point  for stroke in strokes for point in stroke])
        (grid, dmap, r_points) = distance_map(points, dim)
        self.grid = grid
        self.distance_map = dmap
        self.rasterized_points = r_points
        self.dimension = dim
        super(ImageTemplate, self).__init__(strokes, name, timestamps)


def convert_to_image(template):
    return ImageTemplate(template.strokes, template.name, template.timestamps)

def multiple_to_image(templates):
    return ImageTemplate([stroke for t in templates for stroke in t.strokes],
                         [templates[0].name],
                         [stamp for t in templates for stamp in t.timestamps])

# ImageTemplate initialization functions.

def inflate_points(points, min_box_dim=48):
    bbox = bounding_box(points)
    width = box_width(bbox)
    height = box_height(bbox)
    moved = points - bbox[0]
    dim = min_box_dim - 1  # points must fit within 48x48 grid
    inflation = 1/np.max([width/dim, height/dim]) # 1/" prevents DivideByZero
    return np.array(map(lambda point: 
            np.dot(np.diag([inflation]*2), point), moved)).astype(int)

def distance_map(points, dim=48):
    if len(points) == 1: 
        inflated = np.array(([dim/2, dim/2],))
    else:
        centered = points - np.mean(points, axis=0) + np.array([24,24])
        inflated = inflate_points(centered, dim)
    grid = np.zeros([dim, dim])
    for point in inflated:
        grid[point[0],point[1]] = 1
    dist_map = ndimage.morphology.distance_transform_edt(1 - grid)
    return (grid, dist_map, inflated.astype(int))
        
# Distance functions

def mod_hauss_distance(i_tempA, i_tempB):
    assert i_tempA.dimension == i_tempB.dimension

    directed_distances = [0.0, 0.0]
    for i, (temp1, temp2) in enumerate([(i_tempA, i_tempB), (i_tempB, i_tempA)]):
        sum = 0.0
        for p in temp1.rasterized_points:
            sum += temp2.distance_map[p[0], p[1]]
        directed_distances[i] = sum/len(temp1.rasterized_points)
    
    return np.max(directed_distances) / (np.sqrt(2) * i_tempA.dimension)
    
def list_classification(unknown, training):
    distances = [(mod_hauss_distance(unknown, t), label) for
                 t in training]
    return max(distances)
    
