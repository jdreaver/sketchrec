from utilities import *
import numpy as np
from collections import defaultdict

def equation_lines(templates, bounding_boxes=None):
    """ 
    This functions produces a list of a list of ints which correspond
    to the equation lines of a set of templates from the same page.
    """
    
    distance_threshold = 300 # in pixels
    time_threshold = 3000    # in ms
    
    if bounding_boxes is None:
        bounding_boxes = [bounding_box(t.points) for t in templates]
    avg_width = np.mean([box_width(bb) for bb in bounding_boxes])
    avg_height = np.mean([box_height(bb) for bb in bounding_boxes])

    # Create initial clusters
    lines = []
    current_line = [0]
    for i in range(1, len(templates)):
        (t1, t2) = (templates[i], templates[i-1])
        distance_gap = np.linalg.norm(t2.points[0] - t1.points[0])
        time_gap = t2.timestamps[0, 0] - t1.timestamps[-1, -1]

        if distance_gap > distance_threshold or time_gap > time_threshold:
            lines.append(current_line)
            current_line = [i]
        else:
            current_line.append(i)
    
    lines.append(current_line)
    line_boxes = []
    for line in lines:
        line_boxes.append(combine_boxes([bounding_boxes[i] for i in line]))
    
    # Merge likely clusters
    i = 0
    while i < len(lines):
        j = i+1
        while j < len(lines):
            (b1, b2) = (line_boxes[i], line_boxes[j])
            horiz_dist = np.min([b1[0, 0] - b2[1, 0], b2[0, 0] - b1[1, 0]])
            vert_dist = np.min([b1[0, 1] - b2[2, 1], b2[0, 1] - b1[2, 1]])
            
            if all([horiz_dist < 3 * avg_width, horiz_dist > -avg_width * 0.5,
                   vert_dist < -avg_height * 2.0/3.0]):
                line_boxes[i] = combine_boxes([line_boxes[i], line_boxes[j]])
                lines[i].extend(lines[j])
                line_boxes.pop(j)
                lines.pop(j)
                j -= 1
            j += 1
        i += 1
    return lines

# Feature calculations
def equation_stroke_widths(templates, equations, boxes):
    """
    Sets the width of a stroke to the max if it's actual width and
    0.3 times the avg stroke height in the equation.
    """
    widths = np.zeros(len(templates))
    
    for line in equations:
        avg_height = np.mean([box_height(boxes[i]) for i in line])
        for i in line:
            widths[i] = np.max([box_width(boxes[i]), avg_height * 0.3])
    return widths

def feature_calculation(i, j, temp1, temp2):
    """
    Computes the pairwise features between two strokes.
    """
    (points1, points2) = (temp1.points, temp2.points)
    # Min and max pairwise point distances and centroid distance
    distances = [np.linalg.norm(p1 - p2) 
                 for p1 in points1 
                 for p2 in points2]
    min_distance = np.min(distances)
    max_distance = np.max(distances)

    (cent1, cent2) = (np.mean(points1, axis=0), np.mean(points2, axis=0))
    centroid_distance = np.linalg.norm(cent1 - cent2)
    
    # Find overlap
    boxes = [bounding_box(points1), bounding_box(points2)]
    boxes = sorted(boxes, key=box_x)
    horiz_overlap = box_width(boxes[0]) + box_x(boxes[0]) - box_x(boxes[1])
    boxes = sorted(boxes, key=box_y)
    vert_overlap = box_height(boxes[0]) + box_y(boxes[0]) - box_y(boxes[1])

    # Simple time gap
    time_gap = temp2.timestamps[0,0] - temp1.timestamps[-1,-1]

    return (i, j, min_distance, max_distance, centroid_distance,
            horiz_overlap, vert_overlap, time_gap)
    

def compute_features_equation(templates):
    """
    If two strokes are in the same equation and their widths overlap,
    then compute their features.
    """
    lines = equation_lines(templates)
    boxes = np.array([bounding_box(t.points) for t in templates])
    widths = equation_stroke_widths(templates, lines, boxes)
    
    
    
    features = []
    for line in lines:
        for index, i in enumerate(line):
            for j in line[index + 1:]:
                vectors = sorted([(box_x(boxes[i]), widths[i]),  
                                 (box_x(boxes[j]), widths[j])])
                if vectors[1][0] - vectors[0][0] < vectors[0][1]:
                    features.append(feature_calculation(i, j,
                                    templates[i], templates[j]))
    return features
                
def groups_to_join_graph(groups):
    """
    Takes a set of groups and converts them to a graph. Ex:
    1               \
    2,3      ------- \   {1:[1], 2:[2, 3], 3:[2, 3], 4:[4, 5, 6] ...} 
    4,5,6    ------- /
    7               /
    """
    join_graph = defaultdict(list)
    for group in groups:
        for i in group:
            join_graph[i] = group

    # This assertion is to verify the integrity of the .grp files.
    assert len(join_graph) == sum([len(g) for g in groups])
    return join_graph

def join_graph_to_groups(join_graph):
    return sorted([v for v in join_graph.values()])

def features_to_classifier_input(features, join_graph):
    X, y = [], []
    X = [f[2:] for f in features]
    y = [1 if f[1] in join_graph[f[0]] else -1 for f in features]
    return (X,y)

def clf_results_to_join_graph(raw_features, results, num_temps):
    join_graph = dict((i, [i]) for i in range(num_temps))
    for n, result in enumerate(results):
        if result == 1:
            (i, j) = raw_features[n][:2]
            join_graph[j] = sorted(join_graph[j] + join_graph[i])
            join_graph[i] = sorted(join_graph[i] + join_graph[j])
    return join_graph_to_groups(join_graph)



