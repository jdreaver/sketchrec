import image_template
from template import Template

"""
This file contains the definitions for import/export functions.
"""

def single_stroke_unlabeled_file(path):
    templates = []
    with open(path, 'r') as f:
        num_strokes = int(f.readline())
        for i in range(num_strokes):
            stroke = []
            timestamps = []
            num_points = int(f.readline().rstrip())
            for j in range(num_points):
                (x, y, a, b, c, time) = map(int, f.readline().split('\t'))
                stroke.append([x,y])
                timestamps.append(time)
            templates.append(Template([stroke], [timestamps]))
    return templates

def templates_from_file(path):
    """
    UNFINISHED
    There are three types of files:
    1. Single stroke, unlabeled templates.
    2. Multi stroke, unlabeled templates.
    3. Single stroke, labeled
    4. Multi stroke, lebeled

    This function checks the type and calls the next functions
    accordingly.
    """
    
    with open(path, 'r') as f:
        num_points = file.readline().rstrip()
