from math import sin, cos, sqrt, pi

import pyglet

import settings, tools


class SelectionTriangle(object):
    def __init__(self, parent_unit):
        self.parent = parent_unit
        self.init_graphic()
        

    def init_graphic(self):
        unit_origin = -100, -100
        unit_radius = self.parent.radius
        batch = self.parent.batch
        equilateral_vertices = tools.get_equilateral_vertices(unit_origin, unit_radius)
        self.graphic = batch.add_indexed(3, pyglet.gl.GL_LINES, settings.MIDGROUND, [0, 1, 1, 2, 2, 0],
                        ('v2f', equilateral_vertices),
                        ('c3B', (0, 255, 0, 0, 255, 0, 0, 255, 0))
                        )

    def update(self, dt):
        sr = self.parent.selection_rotation
        ss = self.parent.selection_scale
        current_location = self.parent.x, self.parent.y
        self.graphic.vertices = tools.rotate_triangle((0, 0), 
                                  self.parent.image_factor*self.parent.radius * ss,
                                  sr,
                                  current_location)