## THE WILLIAM'S_FIRST_PYGLET_RTS CHEERLEADING COMMENT SECTION
# Noun phrases for data attributes and variables, verbs or prepositions begin
# methods and functions
#
# This could be a fun experiment or it could be a "neat game" or it could be an
# actual Complex, Competitive Real Time Strategy. In a few years it could even 
# be "An RTS Engine for Pyglet (and Cocos2D). Keep refactoring and cleaning up
# so that it isn't intercoupled into one hopeless mess. Good work so far,
# especially on the small, visible refinements.
#
## TO OTHERS
#
# Send fun pyglet tips and tricks, interesting comments, or teaching criticisms
# to wrschuller at gmail. 


from random import choice, randint
from math import sqrt

import pyglet
from pyglet.window import mouse
from pyglet.gl import *

import tools, settings, camera
from selection import mouseselect as ms
from units import tier_one, orders, doodads
from collision import CollisionManager
from resources import mote

class ParadeGround(object):
    def __init__(self):
        self.window = camera.CameraWindow()
        self.batch = pyglet.graphics.Batch()
        self.window.set_handler("on_draw", self.on_draw)
        self.all_graphics = []
        
        # make units
        self.unit_controller = orders.UnitController(self.window)
        self.unit_controller.load_units([tier_one.Sparkle] * 50)
        self.unit_controller.add_observer(self.window.cam)
        self.window.push_handlers(self.unit_controller)
        self.window.push_handlers(self.unit_controller.keys)
        pyglet.clock.schedule_interval(self.unit_controller.update, settings.FRAMERATE)
        
        # TODO: A level/map class for each stage
        self.all_graphics.append(doodads.MapBorder(img=mote, 
                                                   x=0, 
                                                   y=0, 
                                                   group=settings.BACKGROUND, 
                                                   batch=self.batch)
                                                   )
        
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
        self.unit_controller.batch.draw()
        
if __name__ == '__main__':
    game = ParadeGround()
    game.execute()