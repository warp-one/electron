from random import randint
from math import sqrt

import pyglet

from __init__ import ThinkingUnit, Speed, BasicUnit
from shape import Circle, Rectangle
from tools import transform_vertex_list, get_equilateral_vertices, get_rand_RGBs, rotate_triangle
import settings

class Sparkle(ThinkingUnit, Circle):

    size = 24
    radius = size/2
    image_factor = 1.4
    selection_scale = 1.3 * image_factor
    BASE_SPEED = 150.
    MAX_SPEED = 500.

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
        
    def tick_graphics(self, dt):
        super(Sparkle, self).tick_graphics(dt)
        x, y = self.x, self.y
        self.flat_poly.vertices = rotate_triangle((0, 0), self.radius*self.image_factor, self.rotation, (x, y))
        
        
    def update(self, dt):
        super(Sparkle, self).update(dt)
        

        #self.flat_poly.colors = list(get_rand_RGBs(lower=40)) + list(get_rand_RGBs(lower=180)) + list(get_rand_RGBs(lower=222))

class Wall(ThinkingUnit, Rectangle):

    immobile = True

    def __init__(self, *args, **kwargs):
        super(Wall, self).__init__(*args, **kwargs)
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
        vertices = [self.left, self.top, self.right, self.top,
                    self.right, self.top, self.right, self.bottom,
                    self.right, self.bottom, self.left, self.bottom,
                    self.left, self.bottom, self.left, self.top]
        self.flat_poly.vertices = vertices
        
class Pyramid(Wall):

    w, h = 100, 100

    def __init__(self, *args, **kwargs):
        side_normal = (self.w + self.h)/2
        self.z = randint(side_normal, side_normal*2)
        super(Pyramid, self).__init__(*args, **kwargs)
        
        
    def init_graphics(self):
        vertices = [self.left, self.top, 0, self.right, self.top, 0,
                    self.right, self.top, 0, self.right, self.bottom, 0,
                    self.right, self.bottom, 0, self.left, self.bottom, 0,
                    self.left, self.bottom, 0, self.left, self.top, 0]
        vertices.extend([self.x, self.y, self.z, self.left, self.top, 0,
                         self.x, self.y, self.z, self.right, self.top, 0,
                         self.x, self.y, self.z, self.right, self.bottom, 0,
                         self.x, self.y, self.z, self.left, self.bottom, 0])
        self.flat_poly = self.batch.add(16, pyglet.gl.GL_LINES, settings.FOREGROUND,
                                        ('v3f/stream', vertices),
                                        ('c3B', tuple([randint(50, 255)]*len(vertices))
                                        ))
        self.graphics.append(self.flat_poly)
        
    def update(self, dt):
        vertices = [self.left, self.top, 0, self.right, self.top, 0,
                    self.right, self.top, 0, self.right, self.bottom, 0,
                    self.right, self.bottom, 0, self.left, self.bottom, 0,
                    self.left, self.bottom, 0, self.left, self.top, 0]
        vertices.extend([self.x, self.y, self.z, self.left, self.top, 0,
                         self.x, self.y, self.z, self.right, self.top, 0,
                         self.x, self.y, self.z, self.right, self.bottom, 0,
                         self.x, self.y, self.z, self.left, self.bottom, 0])
        self.flat_poly.vertices = vertices
    