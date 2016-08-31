from random import randint
from math import sqrt

import pyglet

from __init__ import ThinkingUnit, Speed, BasicUnit
from shape import Circle, Rectangle
from tools import transform_vertex_list, get_equilateral_vertices, get_rand_RGBs
import settings

class Sparkle(ThinkingUnit, Circle):

    size = 24
    radius = size/2
    image_factor = 1.4
    selection_scale = 1.3 * image_factor
    BASE_SPEED = 150.

    def __init__(self, *args, **kwargs):
        super(Sparkle, self).__init__(*args, **kwargs)
        
        self.selectable = True
        self.color = [200, 200, 200]
        if self.team:
            if self.team == "Player":
                self.color = settings.PLAYER_COLOR
            elif self.team == "CPU":
                self.color = settings.CPU1_COLOR
        
        self.init_graphics()
        self.statuses[Speed.name] = Speed(self)
        
    def init_graphics(self):
        x, y = self.x, self.y
        poly_vertices = get_equilateral_vertices((x, y), self.size/3)
        self.flat_poly = self.batch.add(3, pyglet.gl.GL_TRIANGLES, self.group,
                                        ('v2f/stream', poly_vertices),
                                        ('c3B', (50, 50, 255, 50, 50, 255,
                                                 50, 50, 255))
                                        )
        self.flat_poly.colors = self.color*3
        self.graphics.append(self.flat_poly)
        
    def update(self, dt):
        super(Sparkle, self).update(dt)
        #self.flat_poly.colors = list(get_rand_RGBs(lower=40)) + list(get_rand_RGBs(lower=180)) + list(get_rand_RGBs(lower=222))

class Wall(ThinkingUnit, Rectangle):
    def __init__(self, *args, **kwargs):
        super(Wall, self).__init__(*args, **kwargs)
        self.x, self.y = 200, 200
        self.init_graphics()
        
    def init_graphics(self):
        x, y = self.x, self.y
        vertices = [self.left, self.top, self.right, self.top,
                    self.right, self.top, self.right, self.bottom,
                    self.right, self.bottom, self.left, self.bottom,
                    self.left, self.bottom, self.left, self.top]
        print vertices
        self.flat_poly = self.batch.add(8, pyglet.gl.GL_LINES, settings.FOREGROUND,
                                        ('v2f/stream', vertices),
                                        ('c3B', tuple([100]*(3*len(vertices)/2))
                                        ))
        self.graphics.append(self.flat_poly)
        
    def update(self, dt):
        self.velocity = self.current_speed * dt
        for i, p in enumerate(self.flat_poly.vertices):
            if self.x != self.old_x or self.y != self.old_y:
                self.old_x, self.old_y = self.x, self.y

