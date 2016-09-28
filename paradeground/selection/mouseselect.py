import math

from numpy.linalg import inv, norm
from numpy import array, matrix, subtract, dot, cross


import pyglet
from pyglet.window import mouse
from pyglet.gl import *

import settings, tools

def normalize(v):
    n = norm(v)
    if n == 0:
        return v
    return v/n

class MousePicker(object):

    def __init__(self, camera):
        self.camera = camwin
        self.viewport = (GLint*4)() 
        self.model_matrix = (GLfloat*16)()
        self.projection_matrix = (GLfloat*16)()
        self.current_ray = None
        self.mouse_x, self.mouse_y = 0, 0
        
    def update(self, dt):
        self.viewport = (GLint*4)()
        self.current_ray = self.get_mouse_ray()
        
    def get_mouse_ray(self):
        self.mouse_x, self.mouse_y = self.camera.mouse_x, self.camera.mouse_y
        
        
class MouseSelector(object):
    def __init__(self, parent_camera):
        self.batch = pyglet.graphics.Batch()
        self.selector_graphic = SelectorRectangle(self.batch)
        self.x, self.y = 0, 0
        self.parent = parent_camera
        
        self.graphic = self.batch.add(2, pyglet.gl.GL_LINES, None,
                                        ('v3f/stream', (0, 0, 0, 0, 0, 0)),
                                        ('c3B/stream')
                                      )
        
    def get_plane_from_xy(self, x, y):
        mx = 2. * x/self.parent.w - 1.
        my = 2. * y/self.parent.h - 1.
        ray_nds = array((mx, my))
        ray_clip = array((mx, my, -1., 1.))
        model_matrix = self.parent.view_matrix
        projection_matrix = self.parent.perspective_matrix
        ray_eye = dot(inv(projection_matrix), ray_clip)
        ray_eye = array((ray_eye[0], ray_eye[1], -1., 0.))
        ray_wor = dot(inv(model_matrix), ray_eye)
        ray_wor = array((ray_wor[0], ray_wor[1], ray_wor[2], 0))
        ray_wor = normalize(ray_wor)
        #gluUnProject()
        #https://www.opengl.org/archives/resources/faq/technical/glu.htm#0070
        #https://www.opengl.org/archives/resources/faq/technical/selection.htm#sele0010
        print "NDS, CLIP, EYE, WOR"
        print ray_nds
        print ray_clip
        print ray_eye
        print ray_wor
        self.pick_ray = ray_wor
        _D = self.pick_ray
        O = array((self.parent.x, self.parent.y, self.parent.z, 1))
        d = 0
        _n = array((0, 0, 1, 0))
        t = -(dot(O, _n) + d)/(dot(_D, _n))
        xyz = O + _D*t
        self.graphic.vertices = [O[0], O[1], O[2], xyz[0], xyz[1], xyz[2]]
        return xyz[0], xyz[1]
        
    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & mouse.LEFT:
            if self.parent.mode == 3:
                x, y = self.get_plane_from_xy(x, y)
            else:
                x += self.parent.x
                y += self.parent.y
                
            self.selector_graphic.adjust_origin(x, y)
            self.selector_graphic.adjust_final(x, y)
            
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.parent.mode == 3:
            x, y = self.get_plane_from_xy(x, y)
        else:
            x += self.parent.x
            y += self.parent.y
        if buttons & mouse.LEFT:
            self.selector_graphic.adjust_final(x, y)
            
    def on_mouse_release(self, x, y, buttons, modifiers):
        x += self.parent.x
        y += self.parent.y
        if buttons & mouse.LEFT:
            self.selector_graphic.hide()

            

class SelectorRectangle(object):
    def __init__(self, batch):
        self.batch = batch
        self.create_rect()
        self.init_xy = [0, 0]
        self.final_xy = [0, 0]
        
        pyglet.clock.schedule_interval(self.update, settings.FRAMERATE)
    
    def is_visible(self):
        pass
      
    def hide(self):
        self.adjust_origin(-10, -10)
        self.adjust_final(-10, -10)
        
    def create_rect(self):
        self.graphic = self.batch.add(4, pyglet.gl.GL_LINE_LOOP, None,
                                        ('v2f/stream', (0, 0, 0, 0, 0, 0, 0, 0)),
                                        ('c3B/stream')
                                      )

    def adjust_origin(self, x, y):
        self.graphic.vertices[:2] = [x, y]
        self.init_xy = [x, y]
        
    def adjust_final(self, x, y):
        a, b = self.init_xy
        self.graphic.vertices[2:] = [x, b, x, y, a, y]
        self.final_xy = [x, y]
        
    def update(self, dt):
        self.graphic.colors = list(tools.get_rand_RGBs()) + list(tools.get_rand_RGBs()) + list(tools.get_rand_RGBs()) + list(tools.get_rand_RGBs())
