import image_template
import os
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

## Static solver database I/O

def load_group_file(path):
    groups = []
    with open(path, 'r') as f:
        num_groups = int(f.readline())
        for i in range(num_groups):
            groups.append(map(int, f.readline().split('\t')))
    return groups

def load_label_file(path):
    labels = []
    with open(path, 'r') as f:
        num_labels = int(f.readline())
        for i in range(num_labels):
            labels.append(f.readline().rstrip())
    return labels

def get_labeled_filenames(label_base):
    labeled_files = []
    for root, dirs, files in os.walk(label_base, topdown=False):
        for f in [name for name in files if '.grp' in name]:
            name = os.path.splitext(f)[0]
            full = os.path.join(root, f)
            pen = os.path.split(os.path.dirname(full))[1]
            labeled_files.append((pen, name))
    return sorted(labeled_files)

def load_all_label_files(template_base, label_base):
    templates_by_file = []
    labeled_files = get_labeled_filenames(label_base)
    for (pen, f_name) in labeled_files:
        temp_file = os.path.join(template_base, pen, f_name + '.iv')
        group_file = os.path.join(label_base, pen, f_name + '.grp')
        label_file = os.path.join(label_base, pen, f_name + '.lbl')
        templates = single_stroke_unlabeled_file(temp_file)
        groups = load_group_file(group_file)
        labels = load_label_file(label_file)
        templates_by_file.append((pen, f_name, templates, groups, labels))
    return templates_by_file
    

        
