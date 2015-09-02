from random import choice

import pyglet
from pyglet.window import mouse, key

import tools
import settings,resources

number_keys = [key._1, key._2, key._3, key._4]

class UnitController(object):
    def __init__(self, window):
        self.batch = pyglet.graphics.Batch()
        self.all_units = []
        self.init_xy = (0, 0)
        self.final_xy = (0, 0)
        self.controlled_window = window

        self.to_select = []
        self.observers = []
        
        self.keys = key.KeyStateHandler()
        self.control_groups = []
        self.key_repeat_timer = 0
        self.last_key_pressed = None
        for k in number_keys:
            self.control_groups.append([])
        
    def on_key_press(self, button, modifiers):
        if button == self.last_key_pressed:
            self.repeat = True
        else:
            self.repeat = False
        if button in number_keys:
            control_group_index = number_keys.index(button)
            if modifiers & key.LCTRL:
                self.control_groups[control_group_index] = self.get_selected_units()
            else:
                if self.repeat and self.key_repeat_timer <= 1.:
                    self.notify("CENTER CAMERA")
                    
                self.to_select = self.control_groups[number_keys.index(button)][:]
                self.run_selection()
                self.key_repeat_timer = 0

        self.last_key_pressed = button
            

    def on_mouse_press(self, x, y, buttons, modifiers):
        x += self.wx
        y += self.wy
        if buttons & mouse.LEFT:
            self.init_xy = (x, y)
        if buttons & mouse.LEFT:
            self.init_xy = (x, y)

        if buttons & mouse.RIGHT:
            self.give_move_command(self.get_selected_units(), (x, y))
            
    # an inefficiency here...        
    def get_selected_units(self):
        selected_units = []
        for u in self.all_units:
            if u.is_selected():
                selected_units.append(u)
        return selected_units
            
    def on_mouse_release(self, x, y, buttons, modifiers):
        x += self.wx
        y += self.wy
        if buttons & mouse.LEFT:
            self.final_xy = (x, y)
            if self.keys[key.LSHIFT]:
                for u in self.all_units:
                    if u.is_selected():
                        self.to_select.append(u)
            if self.final_xy == self.init_xy:
                self.select_from_point()
            else:
                self.select_in_area()
        
    def load_units(self, unit_list):
        for u in unit_list:
            new_unit = u(self, img=resources.mote, x=50., y=50., 
                         batch=self.batch, 
                         group=settings.FOREGROUND)
            self.all_units.append(new_unit)
    
    def kill_units(self, unit_list):
        for u in unit_list:
            self.all_units.remove(u)
            # u.spawn_death_animation()
            u.delete()
            
    def run_selection(self):
        for u in self.all_units:
            u.deselect()
        while self.to_select:
            self.to_select.pop().select()
            
    def select_from_point(self):
        for u in self.all_units:
            if tools.get_distance(self.init_xy, (u.x, u.y)) <= u.RADIUS:
                if not u.is_selected():
                    self.to_select.append(u)
                elif self.keys[key.LSHIFT] and u.is_selected():
                    self.to_select.remove(u)
#            else:
#                if self.keys[key.LSHIFT] or self.keys[key.RSHIFT]:
#                    self.to_select.append(u)
        self.run_selection()
            
    def select_in_area(self):
        in_area = []
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
            if u.x >= rect_left and u.x <= rect_right and u.y >= rect_bot and u.y <= rect_top:
                in_area.append(u)
             
        if self.keys[key.LSHIFT]:
            all_selected = True
            for u in in_area:
                if not u.is_selected():
                    all_selected = False
            if all_selected:
                for u in in_area:
                    self.to_select.remove(u)
            else:
                for u in in_area:
                    if not u.is_selected():
                        self.to_select.append(u)
        else:
            for u in in_area:

                self.to_select.append(u)
        self.run_selection()
            
    def give_move_command(self, unit_list, destination):
        for u in unit_list:
            u.receive_move_command(destination)
           
    def update(self, dt):
        cam = self.controlled_window.cam
        self.wx, self.wy = cam.x, cam.y
        for u in self.all_units:
            u.update(dt)
        self.key_repeat_timer += dt
        
    def add_observer(self, observer):
        self.observers.append(observer)
        
    def remove_observer(self, observer):
        self.observers.remove(observer)
        
    def notify(self, event):
        for o in self.observers:
            o.on_notify(choice(self.get_selected_units()), event)
