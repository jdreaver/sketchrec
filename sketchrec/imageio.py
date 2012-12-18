"""
This file contains the definitions for import/export functions.
"""

import os
from sketchrec.template import Template

def single_stroke_unlabeled_file(path):
    
    """
    Opens a raw file with single strokes and time stamps.
    """
    
    templates = []
    with open(path, 'r') as f:
        num_strokes = int(f.readline())
        for i in range(num_strokes):
            stroke = []
            timestamps = []
            num_points = int(f.readline().rstrip())
            for j in range(num_points):
                (x, y, a, b, c, time) = map(int, f.readline().split('\t'))
                stroke.append([x, y])
                timestamps.append(time)
            templates.append(Template([stroke], timestamps=[timestamps]))
    return templates

## Static solver database I/O

def load_group_file(path):

    """
    Loads the .grp file in path. Returns groups.
    """
    
    groups = []
    with open(path, 'r') as f:
        num_groups = int(f.readline())
        for i in range(num_groups):
            groups.append(map(int, f.readline().split('\t')))
    return groups

def load_label_file(path):

    """
    Returns list of labels in the .lbl file from path.
    """
    
    labels = []
    with open(path, 'r') as f:
        num_labels = int(f.readline())
        for i in range(num_labels):
            labels.append(f.readline().rstrip())
    return labels

def get_labeled_filenames(label_base):
    
    """
    Scans the database for all labeled file names.
    """
    
    labeled_files = []
    for root, dirs, files in os.walk(label_base, topdown=False):
        for f in [name for name in files if '.grp' in name]:
            name = os.path.splitext(f)[0]
            full = os.path.join(root, name)
            labeled_files.append(full)
    return sorted(labeled_files)

def load_page(base_file):
    templates = single_stroke_unlabeled_file(base_file + '.iv')
    groups = load_group_file(base_file + '.grp')
    labels = load_label_file(base_file + '.lbl')
    return (templates, groups, labels)
    
# def get_labeled_filenames(label_base):
    
#     """
#     Scans the database for all labeled file names.
#     """
    
#     labeled_files = []
#     for root, dirs, files in os.walk(label_base, topdown=False):
#         for f in [name for name in files if '.grp' in name]:
#             name = os.path.splitext(f)[0]
#             full = os.path.join(root, f)
#             pen = os.path.split(os.path.dirname(full))[1]
#             labeled_files.append((pen, name))
#     return sorted(labeled_files)



# def load_all_label_files(template_base, label_base):

#     """
#     Returns all labeled files in database.
#     """
    
#     templates_by_file = []
#     labeled_files = get_labeled_filenames(label_base)
#     for (pen, f_name) in labeled_files:
#         temp_file = os.path.join(template_base, pen, f_name + '.iv')
#         group_file = os.path.join(label_base, pen, f_name + '.grp')
#         label_file = os.path.join(label_base, pen, f_name + '.lbl')
#         templates = single_stroke_unlabeled_file(temp_file)
#         groups = load_group_file(group_file)
#         labels = load_label_file(label_file)
#         templates_by_file.append((pen, f_name, templates, groups, labels))
#     return templates_by_file
    

        
