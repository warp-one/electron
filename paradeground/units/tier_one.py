from random import randint
from math import sqrt

import pyglet

from __init__ import BasicUnit
from tools import transform_vertex_list, get_equilateral_vertices, get_rand_RGBs

class Sparkle(BasicUnit):

    SELECTION_SCALE = 1.3

    def __init__(self, *args, **kwargs):
        super(Sparkle, self).__init__(*args, **kwargs)
        
        self.selectable = True
        self.SIZE = 32
        self.RADIUS = self.SIZE/2
        self.init_graphics()
        
    def init_graphics(self):
        x, y = self.x, self.y
        poly_vertices = get_equilateral_vertices((x, y), self.SIZE/3)
        self.flat_poly = self.batch.add(3, pyglet.gl.GL_TRIANGLES, self.group,
                                        ('v2f/stream', poly_vertices),
                                        ('c3B', (50, 50, 255, 50, 50, 255,
                                                 50, 50, 255))
                                        )
        
        self.graphics.append(self.flat_poly)
        
    def update(self, dt):
        super(Sparkle, self).update(dt)
        self.flat_poly.colors = list(get_rand_RGBs(lower=40)) + list(get_rand_RGBs(lower=180)) + list(get_rand_RGBs(lower=222))
