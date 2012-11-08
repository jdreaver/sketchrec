class Template(object):
    """
    """
    
    def __init__(self, strokes, timestamps=[]):
        self.strokes = strokes
        self.timestamps = timestamps
        
    def is_single_stroke(self):
        return len(self.strokes) == 1
        

        
