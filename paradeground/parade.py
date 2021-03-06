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

## IDEAS
#
# charge seeking negation as a joyous exercise
# glitter glued onto construction paper
# 


from random import choice, randint
from math import sqrt

import pyglet
from pyglet.window import mouse
from pyglet.gl import *

import tools, settings, camera
from selection import mouseselect as ms
from units import tier_one, orders, doodads, power_grid
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
        sparkles = [tier_one.Sparkle( 
                         team="Player",
                         img=mote,
                         x=randint(100, 1000), 
                         y=randint(100, 1000), 
                         batch=self.unit_controller.batch, 
                         group=settings.FOREGROUND) for _ in range(40)]
        evil_sparkles = [tier_one.Sparkle( 
                         team="CPU",
                         img=mote, 
                         x=randint(100, 1000), 
                         y=randint(100, 1000), 
                         batch=self.unit_controller.batch, 
                         group=settings.FOREGROUND) for _ in range(5)]
                         

        self.unit_controller.load_units(sparkles)
        self.unit_controller.load_units(evil_sparkles)
        new_grids = [power_grid.PowerGrid(
                         team=None,
                         img=mote, 
                         x=p, 
                         y=p, 
                         batch=self.unit_controller.batch, 
                         group=settings.FOREGROUND) for p in range(500, 2000, 500)]                         
        self.unit_controller.load_units(new_grids)
        
        walls = [tier_one.Pyramid(a, b,
                         team=None,
                         img=mote, 
                         x=c, 
                         y=d, 
                         batch=self.unit_controller.batch, 
                         group=settings.FOREGROUND) 
                     for a, b, c, d in [(400, 400, 1000, 500),
                                        (300, 500, 1200, 1600),
                                        (100, 100, 1350, 400),
                                        (100, 100, 1450, 400),
                                        (130, 130, 1450, 515)]                         
                ]
        self.unit_controller.load_units(walls)
#        for wall in walls:
#            self.unit_controller.collision_manager.grid.move(wall, 200, 200)
#        grids[0].x, grids[0].y = 750, 800
#        grids[0].change_size(1200, 300, strand_frequency=20)
        new_grids[1].change_size(1200, 250)
        self.unit_controller.collision_manager.grid.collision = True
        self.unit_controller.add_observer(self.window.cam)
        self.window.push_handlers(self.unit_controller)
        self.window.push_handlers(self.unit_controller.keys)
        
        self.window_controller = orders.WindowController(self.window)
        self.window.push_handlers(self.window_controller)
        self.window.push_handlers(self.window_controller.keys)
        
        pyglet.clock.schedule_interval(self.unit_controller.update, settings.FRAMERATE)
        
        # TODO: A level/map class for each stage
        self.all_graphics.append(doodads.MapBorder(img=mote, 
                                                   x=0, 
                                                   y=0, 
                                                   group=settings.BACKGROUND, 
                                                   batch=self.batch)
                                                   )
        
    def execute(self):
        pyglet.app.run()
        
    def on_draw(self):
        self.window.clear()
        self.window.cam.apply()
        self.window.mouse_selector.batch.draw()
        if settings.ANTI_ALIASING:
            pyglet.gl.glColor4f(1.0, 0, 0, 1.0)
            glBlendFunc (GL_ONE_MINUS_CONSTANT_COLOR, GL_ONE_MINUS_SRC_ALPHA)                             
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