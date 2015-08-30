import pyglet

def get_equilateral_vertices(center, radius, rotation):
    x, y = center
    r = radius
    a = r/2
    triangle_side = 2*a*sqrt(3)
    bottom_left = x - triangle_side/2, y - a
    bottom_right = x + triangle_side/2, y - a
    top_center = x, y + r
    return (list(bottom_left) + list(bottom_right) + list(top_center))

class SelectionTriangle(object):
    def __init__(self, parent_unit):
        self.parent = parent_unit
    
    def create_graphic(self):
        pass