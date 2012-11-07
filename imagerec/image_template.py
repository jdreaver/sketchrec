import image_calc

class ImageTemplate(object):
    """
    """
    
    def __init__(self, points, dim=48):
        (grid, dmap, points) = image_calc.distance_map(points, dim)
        self.grid = grid
        self.distance_map = dmap
        self.points = points
        
