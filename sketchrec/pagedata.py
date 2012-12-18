import os

from sketchrec.imageio import get_labeled_filenames, load_page

class PageData():
    
    """Class for holding data from one page of work."""
    
    def __init__(self, filename):
        self.filename = filename
        (self.templates, self.groups, self.labels) = load_page(filename)
        self.pen = os.path.split(os.path.dirname(filename))[1]



def load_all_page_data(base_directory):

    """
    Returns all labeled files in database.
    """
    
    page_data = []
    labeled_files = get_labeled_filenames(base_directory)
    for base_file in labeled_files:
        page_data.append(PageData(base_file))
    return page_data
        
