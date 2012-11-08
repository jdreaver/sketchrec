class Template(object):
    """
    """
    
    def __init__(self, strokes, timestamps=None):
        self.strokes = strokes
        self.points = [p for s in strokes for p in s]
        self.timestamps = timestamps
        
    def is_single_stroke(self):
        return len(self.strokes) == 1

    def has_time_stamps(self):
        return self.timestamps is None
        

        
