import pyglet
from pyglet.window import mouse

import tools
from resources import mote, thirty
from settings import FOREGROUND

class UnitController(object):
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.all_units = []
        self.init_xy = (0, 0)
        self.final_xy = (0, 0)
        
        self.background = pyglet.graphics.OrderedGroup(0)
        self.midground = pyglet.graphics.OrderedGroup(1)
        self.foreground = pyglet.graphics.OrderedGroup(2)

        pyglet.clock.schedule_interval(self.update, 1/60.)
        
    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons & mouse.LEFT:
            self.init_xy = (x, y)
        if buttons & mouse.RIGHT:
            selected_units = []
            for u in self.all_units:
                if u.is_selected():
                    selected_units.append(u)
            self.give_move_command(selected_units, (x, y))
            
    def on_mouse_release(self, x, y, buttons, modifiers):
        if buttons & mouse.LEFT:
            self.final_xy = (x, y)
            self.select_in_area()

        
    def load_units(self, unit_list):
        for u in unit_list:
            new_unit = u(self, img=mote, x=50, y=50, batch=self.batch, group=FOREGROUND)
            self.all_units.append(new_unit)
    
    def kill_units(self, unit_list):
        for u in unit_list:
            self.all_units.remove(u)
            # u.spawn_death_animation()
            u.delete()
            
    def select_in_area(self):
        x1, y1 = self.init_xy
        x2, y2 = self.final_xy
        if x1 > x2:
            rect_right = x1
            rect_left = x2
        else:
            rect_right = x2
            rect_left = x1
        if y1 > y2:
            rect_top = y1
            rect_bot = y2
        else:
            rect_top = y2
            rect_bot = y1
        for u in self.all_units:
            if u.x >= rect_left and u.x <= rect_right:
                if u.y >= rect_bot and u.y <= rect_top:
                    u.select()
                else:
                    if u.is_selected:
                        u.deselect()
            else:
                if u.is_selected:
                    u.deselect()
            
    def give_move_command(self, unit_list, destination):
        for u in unit_list:
            u.receive_move_command(destination)
           
    def update(self, dt):
        pass