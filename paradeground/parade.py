from random import choice, randint
from math import sqrt

import pyglet
from pyglet.window import mouse
from pyglet.gl import *

import tools, settings, camera
from selection import mouseselect as ms
from units import tier_one, orders
from collision import CollisionManager


class ParadeGround(object):
    def __init__(self):
        self.window = camera.CameraWindow()
        self.batch = pyglet.graphics.Batch()
        self.window.set_handler("on_draw", self.on_draw)
        self.all_graphics = []
        
        # make units
        self.controller = orders.UnitController(self.window)
        self.controller.load_units([tier_one.Sparkle] * 50)
        self.controller.add_observer(self.window.cam)
        self.window.push_handlers(self.controller)
        self.window.push_handlers(self.controller.keys)
        pyglet.clock.schedule_interval(self.controller.update, settings.FRAMERATE)
        self.collision_manager = CollisionManager(self.controller.all_units, 
                                                  (settings.WINDOW_WIDTH,
                                                  settings.WINDOW_HEIGHT))
        self.collision_manager.create_grid()
        self.collision_manager.distribute_units()
        
    def add_rect(self):
        new_rect = self.batch.add(2, pyglet.gl.GL_LINES, None, 
                        ('v2i', (-10, -10, -10, -10)),
                        ('c3B', (0, 0, 255, 0, 255, 0))
                       )
        self.all_graphics.append(new_rect)
        return new_rect
        
    def execute(self):
        pyglet.app.run()
        
    def on_draw(self):
        self.window.clear()
        self.collision_manager.debug()
        self.window.mouse_selector.batch.draw()
        self.window.cam.apply()
        if settings.ANTI_ALIASING:
            pyglet.gl.glColor4f(1.0, 0, 0, 1.0)
            glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)                             
            glEnable (GL_BLEND)                                                            
            glEnable (GL_MULTISAMPLE);                                                     

            glEnable (GL_LINE_SMOOTH);                                                     
            glEnable (GL_POLYGON_SMOOTH);                                                     
            glHint (GL_LINE_SMOOTH_HINT, GL_DONT_CARE)                                     
            glLineWidth (1)                                                                
        self.batch.draw()
        self.controller.batch.draw()
        
if __name__ == '__main__':
    game = ParadeGround()
    game.execute()