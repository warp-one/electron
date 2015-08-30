from random import choice, randint
from math import sqrt

import pyglet
from pyglet.window import mouse

import orders, tier_one, tools, settings

def get_rand_RGBs():
    return (randint(0, 255), randint(0, 255), randint(0, 255))

def get_next_list_item(original, the_list):
    next_index = the_list.index(original) + 1
    if next_index >= len(the_list):
        next_index = 0
    return the_list[next_index]
 

class ParadeGround(object):
    def __init__(self):
        self.window = pyglet.window.Window(width=800, height=600)
        self.mouse_test = MouseSelector()
        self.window.push_handlers(self.mouse_test)
        self.batch = pyglet.graphics.Batch()
        self.window.set_handler("on_draw", self.on_draw)
        self.all_graphics = []
        
        pyglet.clock.schedule_interval(self.update, settings.FRAMERATE)
        
        
        # make units
        self.controller = orders.UnitController()
        self.controller.load_units([tier_one.Sparkle] * 500)
        self.window.push_handlers(self.controller)
        for u in self.controller.all_units:
            pyglet.clock.schedule_interval(u.update, settings.FRAMERATE)
            u.select()
        
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
        self.batch.draw()
        self.mouse_test.batch.draw()
        self.controller.batch.draw()
        
    def update(self, dt):
        pass        
        
                      
        
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
        self.graphic = self.batch.add(2, pyglet.gl.GL_LINES, None,
                                        ('v2i/stream', (35, 35, 55, 55)),
                                        ('c3B/stream', (0, 0, 255, 0, 255, 0))
                                      )

    def adjust_origin(self, x, y):
        self.graphic.vertices[:2] = [x, y]
        
    def adjust_final(self, x, y):
        self.graphic.vertices[2:] = [x, y]
        
    def update(self, dt):
        self.graphic.colors = list(get_rand_RGBs()) + list(get_rand_RGBs())
        
if __name__ == '__main__':
    game = ParadeGround()
    game.execute()