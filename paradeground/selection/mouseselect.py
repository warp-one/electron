import pyglet
from pyglet.window import mouse

import settings, tools

class MouseSelector(object):
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.selector_graphic = SelectorRectangle(self.batch)
        self.x, self.y = 0, 0
        
    def on_mouse_motion(self, x, y, dx, dy):
        self.x, self.y = x, y
    
    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & mouse.LEFT:
            self.selector_graphic.adjust_origin(x, y)
            self.selector_graphic.adjust_final(x, y)
            
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT:
            self.selector_graphic.adjust_final(x, y)
            
    def on_mouse_release(self, x, y, buttons, modifiers):
        if buttons & mouse.LEFT:
            self.selector_graphic.hide()

            

class SelectorRectangle(object):
    def __init__(self, batch):
        self.batch = batch
        self.create_rect()
        
        pyglet.clock.schedule_interval(self.update, settings.FRAMERATE)
    
    def is_visible(self):
        pass
      
    def hide(self):
        self.adjust_origin(-10, -10)
        self.adjust_final(-10, -10)
        
    def create_rect(self):
        self.graphic = self.batch.add(4, pyglet.gl.GL_LINE_LOOP, None,
                                        ('v2i/stream', (0, 0, 0, 0, 0, 0, 0, 0)),
                                        ('c3B/stream')
                                      )

    def adjust_origin(self, x, y):
        self.graphic.vertices[:2] = [x, y]
        self.init_xy = [x, y]
        
    def adjust_final(self, x, y):
        a, b = self.init_xy
        self.graphic.vertices[2:] = [x, b, x, y, a, y]
        
    def update(self, dt):
        self.graphic.colors = list(tools.get_rand_RGBs()) + list(tools.get_rand_RGBs()) + list(tools.get_rand_RGBs()) + list(tools.get_rand_RGBs())
