import numpy as np

class Template(object):
    """
    """
    
    def __init__(self, strokes, name="NO LABEL", timestamps=None):
        self.strokes = strokes
        self.points = np.array([p for s in strokes for p in s])
        self.name = name
        self.timestamps = timestamps
        
    def is_single_stroke(self):
        return len(self.strokes) == 1

    def has_time_stamps(self):
        return self.timestamps is None
        

        
