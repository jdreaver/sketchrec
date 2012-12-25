""" 
This file contains the definition for an ImageTemplate as well as
all of the functions for creating an image template and finding
the distance between two templates.
"""

import numpy as np
from scipy import ndimage
from sketchrec.template import Template
from sketchrec.utilities import bounding_box, box_width, box_height

class ImageTemplate(Template):
    
    """
    Container for image recognizer template.
    
    An image template contains a rasterized set of the template's
    strokes, and the distance transform computed from said rasterized
    points. The distance transform and rasterized coordinates are
    flattened so the hausdorff distances can be more easily computed.
    """
    
    def __init__(self, strokes, name="NO LABEL", timestamps=None, dim=48, resample=True):
        points = np.array([point  for stroke in strokes for point in stroke])
        (grid, dmap, r_points) = distance_map(points, dim, resample)
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

def multiple_to_image(templates, dim=48, resample=True):
    
    """
    Combines the strokes and timestamps of multiple templates into
    a single image template. Assumes each stroke has the same name.
    """
    
    return ImageTemplate([stroke for t in templates for stroke in t.strokes],
                         templates[0].name, 
                         [stamp for t in templates for stamp
                          in t.timestamps],
                         dim=dim, resample=resample)

# ImageTemplate initialization functions.

def inflate_points(points, dim=48):
    
    """
    Takes a set of raw stroke points and scales them to a (default)
    48x48 grid. The points are scaled with the aspect ratio intact.

    Keyword arguments:
    points -- raw sampled points from template
    dim -- width/length of rasterized bitmap in pixels
    """
    
    bbox = bounding_box(points)
    width = box_width(bbox)
    height = box_height(bbox)
    moved = points - bbox[0]
    inflation = 1/np.max([width/(dim - 1),
                          height/(dim - 1)]) # 1/" prevents DivideByZero
    return np.array(map(lambda point: 
            np.dot(np.diag([inflation]*2), point), moved)).astype(int)

def full_upsample(old_points):

    """
    Takes a set of integer-valued points and connects each consecutive
    point by integer-valued jumps. For example:
    points = [[0, 0], [2, 2]]
    full_upsample(points) => [[0,0], [1,1], [2,2]]
    """
    
    points = list(old_points[:])
    i = 1
    while i < len(points):
        (dx, dy) = points[i] - points[i - 1]
        (absx, absy) = (abs(dx), abs(dy))
        (sign_x, sign_y) = (np.sign(dx), np.sign(dy))
        # Insert points until there is no longer a gap between the
        # original points
        while absx > 1 or absy > 1:
            if absx > absy:
                points.insert(i, points[i - 1] + np.array(([sign_x, 0])))
                absx -= 1
            elif absx < absy:
                points.insert(i, points[i - 1] + np.array(([0, sign_y])))
                absy -= 1
            else:
                points.insert(i, points[i - 1] + np.array(([sign_x, sign_y])))
                absx -= 1
                absy -= 1
            i += 1
        i += 1

    return np.array(points)
    
def distance_map(points, dim=48, resample=True):
    
    """
    Computes the distance map given the raw points of a template.

    To compute the distance map, a set of raw points from a
    template (maybe multistroke) is centered and uniformly scaled
    to fit in a dim by dim pixel bitmap.

    Keyword arguments:
    points -- raw sampled points from template
    dim -- width/length of rasterized bitmap in pixels
    """
    
    if len(points) == 1: 
        inflated = np.array(([dim/2, dim/2],))
    else:
        centered = points - np.mean(points, axis=0) + np.array([24, 24])
        inflated = inflate_points(centered, dim)
        if resample:
            inflated = full_upsample(inflated)
    # Remove duplicates whilst preserving order
    seen = set()
    inflated = np.array([p for p in inflated if tuple(p) not in seen
                         and not seen.add(tuple(p))])
    
    grid = np.zeros([dim, dim])
    for point in inflated:
        grid[point[0], point[1]] = 1
    # except IndexError:
    #     print "into: " + repr(into)
    #     print "\npoints: \n" + repr(points)
    #     print "\ncentered: \n" + repr(centered)
    #     print "\ninflated: \n" + repr(inflated)
    #     raise SystemExit
    dist_map = ndimage.morphology.distance_transform_edt(1 - grid)
    return (grid, dist_map, inflated.astype(int))
        
# Distance functions

def list_classification(unknown, training):
    
    """ 
    Return closest training template using MHD.

    Performs nearest-neighbor search on the unkown template to find
    nearest training template. I spent a few hours optimizing this
    one.

    Keyword arguments:
    unknown -- template to be recognized
    training -- list of known templates
    """
    
    min_dist = (1.0 * 1.4142 * unknown.dimension + 1.0, 'ERROR')
    for temp in training:
        dist = max(
            np.sum(unknown.flat_map.take(temp.flat_points))/temp.num_r_points,
            np.sum(temp.flat_map.take(unknown.flat_points))/unknown.num_r_points
            )
        min_dist = min([min_dist, (dist, temp.name)])
    min_dist = (min_dist[0] / (1.4142 * unknown.dimension), min_dist[1])
    return min_dist[1]

def modified_haussdorff_distance(template_a, template_b):
    raw =  max(
            np.sum(template_a.flat_map.take(template_b.flat_points))/template_b.num_r_points,
            np.sum(template_b.flat_map.take(template_a.flat_points))/template_a.num_r_points
            )
    return raw / (1.4142 * template_a.dimension)

def group_centroid(templates):
    points = []
    [points.extend(template.points) for template in templates]
    return np.mean(points, axis=0)


    
