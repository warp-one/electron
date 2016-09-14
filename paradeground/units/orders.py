from random import choice, randint

import pyglet
from pyglet.window import mouse, key

import tools
import settings,resources
from collision import CollisionManager

number_keys = [key._1, key._2, key._3, key._4, key.Q, key.W, key.E, key.R]

class WindowController(object):
    def __init__(self, window):
        self.window = window
        self.window_sizes = [(800, 600), (1024, 768), (1680, 1050)]
        self.current_size = len(self.window_sizes) - 1
        self.keys = key.KeyStateHandler()
        
        
    def on_key_press(self, symbol, modifiers):
        if symbol == key.M:
            self.current_size += 1
            if self.current_size >= len(self.window_sizes):
                self.current_size = 0
            self.window.set_size(*self.window_sizes[self.current_size])
        if symbol == key.F:
            if self.window.fullscreen:
                self.window.set_fullscreen(False)
            else:
                self.window.set_fullscreen(True)
            
class UnitController(object):
    def __init__(self, window):
        self.batch = pyglet.graphics.Batch()
        self.entities = {}
        self.entity_id = 0
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
            
        self.collision_manager = CollisionManager(self.entities.values())
                                       
    def add_entity(self, entity):
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1
        
    def remove_entity(self, entity):
        del self.entities[entity.id]
        
    def get_entity(self, entity_id):
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None
            
    def get_unit_list(self):
        return list(self.entities.values())
            
    # get rid of this        
    def get_close_entity(self, location, e_range=100):
        for entity in self.get_unit_list():
            distance = tools.get_distance(location, (entity.x, entity.y))
            if distance < e_range:
                return entity
        return None
        
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
                self.to_select = self.control_groups[number_keys.index(button)][:]
                if self.repeat and self.key_repeat_timer <= 3.:
                    self.notify(tools.get_average_location(self.to_select), "CENTER CAMERA")
                    
                self.run_selection()
                self.key_repeat_timer = 0
        if button == key.S:
            for u in self.get_selected_units():
                u.arrive()
        if button == key.DELETE:
            to_delete = []
            for u in self.get_selected_units():
                if u.team == "Player":
                    to_delete.append(u)
            self.kill_units(to_delete)

        self.last_key_pressed = button
            

    def on_mouse_press(self, x, y, buttons, modifiers):
        x += self.wx
        y += self.wy
        if buttons & mouse.LEFT:
            self.init_xy = (x, y)

        if buttons & mouse.RIGHT:
            units_to_order = self.get_selected_units()
            if units_to_order:
                origin = tools.get_average_location(units_to_order)
                if modifiers & key.MOD_SHIFT:
                    self.give_move_command(self.get_selected_units(), origin, (x, y), shift=True)
                else:
                    self.give_move_command(self.get_selected_units(), origin, (x, y))
            
    # an inefficiency here...        
    def get_selected_units(self):
        selected_units = []
        for u in self.get_unit_list():
            if u.is_selected():
                selected_units.append(u)
        return selected_units
            
    def on_mouse_release(self, x, y, buttons, modifiers):
        x += self.wx
        y += self.wy
        if buttons & mouse.LEFT:
            self.final_xy = (x, y)
            if self.keys[key.LSHIFT]:
                for u in self.get_unit_list():
                    if u.is_selected():
                        self.to_select.append(u)
            if self.final_xy == self.init_xy:
                self.select_from_point()
            else:
                self.select_in_area()
        
    def load_units(self, unit_list):
        loaded_units = []
        for new_unit in unit_list:
            self.add_entity(new_unit)
            self.collision_manager.grid.add(new_unit)
            # the line below is only doing the team units?
            if new_unit.shape == "circle":
                self.collision_manager.grid.move(new_unit, randint(100, 1700), randint(100, 1700))
            new_unit.current_destination = new_unit.get_location()
            loaded_units.append(new_unit)
        return loaded_units
        
    
    def kill_units(self, unit_list):
        for u in unit_list:
            self.remove_entity(u)
            self.collision_manager.grid.remove(u)
            u.suicide()
            
    def run_selection(self):
        for u in self.get_unit_list():
            u.deselect()
        while self.to_select:
            self.to_select.pop().select()
            
    def select_from_point(self):
        for u in self.get_unit_list():
            if tools.get_distance(self.init_xy, (u.x, u.y)) <= u.radius:
                if not u.is_selected():
                    self.to_select.append(u)
                elif self.keys[key.LSHIFT] and u.is_selected():
                    self.to_select.remove(u)
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
        for u in self.get_unit_list():
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
                        if u.team == "Player":

                            self.to_select.append(u)
        else:
            for u in in_area:
                if u.team == "Player":

                    self.to_select.append(u)
        self.run_selection()
            
    def give_move_command(self, unit_list, origin, destination, shift=False):
        order_angle = 0
        exes = [unit.x for unit in unit_list]
        whys = [unit.y for unit in unit_list]
        min_x = min(exes)
        max_x = max(exes)
        min_y = min(whys)
        max_y = max(whys)
        a, b = destination
        # narrow angles should still be forced move
        if len(unit_list) > 1:
            v1, v2 = tools.closest_two_square_vertices(destination, min_x, max_x, min_y, max_y)
            order_angle = tools.angle_from_three_points(destination, v1, v2)
        internal_move = ((a > min_x and a < max_x) and (b > min_y and b < max_y))
        if shift:
            orders = "MOVE"
        elif internal_move or order_angle > 35:
            orders = "GATHER"
        else:
            orders = "MOVE"
        for u in unit_list:
            u.receive_command(destination, command=orders, origin=origin)
           
    def update(self, dt):
        cam = self.controlled_window.cam
        self.wx, self.wy = cam.x, cam.y
        self.collision_manager.update(dt) # marks colliding units
        for u in list(self.entities.values()):
            if not u in self.collision_manager.grid.colliding_units:
                self.collision_manager.grid.move(u, u.dx, u.dy)
            u.update(dt)
        self.key_repeat_timer += dt
        
    def add_observer(self, observer):
        self.observers.append(observer)
        
    def remove_observer(self, observer):
        self.observers.remove(observer)
        
    def notify(self, unit, event):
        for o in self.observers:
            o.on_notify(unit, event)
