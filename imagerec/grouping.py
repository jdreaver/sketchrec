from utilities import bounding_box, combine_boxes
import numpy as np

def equation_lines(templates):
    """ 
    This functions produces a list of a list of ints which correspond
    to the equation lines of a set of templates from the same page.
    """
    
    distance_threshold = 300 # in pixels
    time_threshold = 3000    # in ms
    
    bounding_boxes = [bounding_box(t.points) for t in templates]
    avg_width = np.mean([bb[1, 0] - bb[0, 0] for bb in bounding_boxes])
    avg_height = np.mean([bb[2, 1] - bb[0, 1] for bb in bounding_boxes])

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
    
    line_boxes = []
    for line in lines:
        line_boxes.append(combine_boxes([bounding_boxes[i] for i in line]))
    
    # Merge likely clusters
    for i in range(1, len(lines)):
        for j in range(i + 1, len(lines)):
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
    return lines
