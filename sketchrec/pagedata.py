import os

from sketchrec.imageio import (get_labeled_filenames, load_page,
                               single_stroke_unlabeled_file)
from sketchrec.grouping import (compute_features_equation,
                                groups_to_join_graph,
                                features_to_classifier_input,
                                group_image_templates)

class PageData():
    
    """Class for holding data from one page of work."""
    
    def __init__(self, filename, labeled=False):
        self.labeled = labeled
        self.groups = self.labels = self.templates = []
        self.filename = filename
        self.filename_base = os.path.splitext(os.path.basename(filename))[0]
        
        if labeled:
            (self.templates, self.groups, self.labels) = load_page(filename)
        else:
            self.templates = single_stroke_unlabeled_file(filename)
            self.labels = ['NO LABEL' for i in range(len(self.templates))]
            
        self.pen = os.path.split(os.path.dirname(filename))[1]
        self.num_temps = len(self.templates)

    def compute_recognition_data(self, dim=48, resample=True):
        # Assign labels to actual template data structure.
        for i, temp in enumerate(self.templates):
            temp.name = self.labels[i]
        self.join_graph = groups_to_join_graph(self.groups)
        self.image_templates = group_image_templates(self.templates,
                                                     self.groups, dim=dim,
                                                     resample=resample)
        self.raw_features = compute_features_equation(self.templates)
        (self.group_features, self.group_labels) = features_to_classifier_input(
            self.raw_features, self.join_graph)
        

def load_all_page_data(base_directory, dim=48, resample=True):

    """
    Returns all labeled files in database.
    """
    
    page_data = []
    labeled_files = get_labeled_filenames(base_directory)
    for base_file in labeled_files:
        page_data.append(PageData(base_file, labeled=True))
    return page_data
