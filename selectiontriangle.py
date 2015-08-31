from math import sin, cos, sqrt, pi

import pyglet

import settings

def apply_point_rotation_matrix(d_theta, point, origin):
    x, y = point
    a, b = origin
    return (x*cos(d_theta) - y*sin(d_theta)) + a, (x*sin(d_theta) + y*cos(d_theta)) + b

def get_equilateral_vertices(origin, radius):
    # the sides of a 30 degree right triangle are 1 : sqrt(3) : 2
    x, y = origin
    a = radius/2
    bottom_left = [x - a*sqrt(3), y - a]
    bottom_right = [x + a*sqrt(3), y - a]
    top_center = [x, y + radius]
    return bottom_left + bottom_right + top_center
    

class SelectionTriangle(object):
    def __init__(self, parent_unit):
        self.parent = parent_unit
        self.rotation = 0
        self.ROTATION_RATE = 1 * pi/180 # radians = degrees * pi/180
        self.init_graphic()
        

    def init_graphic(self):
        unit_origin = -100, -100
        unit_radius = self.parent.RADIUS
        batch = self.parent.batch
        equilateral_vertices = get_equilateral_vertices(unit_origin, unit_radius)
        self.graphic = batch.add_indexed(3, pyglet.gl.GL_LINES, None, [0, 1, 1, 2, 2, 0],
                        ('v2f', equilateral_vertices),
                        ('c3B', (0, 255, 0, 0, 255, 0, 0, 255, 0))
                        )

    def tick_rotation(self):
        self.rotation += self.ROTATION_RATE

    def update(self, dt):
        x, y = self.parent.x, self.parent.y
        self.tick_rotation()
        original_vertices = get_equilateral_vertices((0, 0), self.parent.RADIUS)
        v1 = original_vertices[0], original_vertices[1]
        v2 = original_vertices[2], original_vertices[3]
        v3 = original_vertices[4], original_vertices[5]
        old_vertices = [v1, v2, v3]
        new_vertices = []
        for v in old_vertices:
            new_vertices.extend(list(apply_point_rotation_matrix(self.rotation, v, (x, y))))
        self.graphic.vertices = new_vertices