from math import sqrt, pi, sin, cos, tan, degrees

import pyglet

from tools import *
from selection import selectiontriangle as st
import settings


class BasicUnit(pyglet.sprite.Sprite):
    def __init__(self, controller, *args, **kwargs):
        super(BasicUnit, self).__init__(*args, **kwargs)
        
        self.controller = controller
        self.current_command = None
        self.current_destination = None
        self.graphics = []
        self.group = settings.FOREGROUND
        self.sgroup = settings.MIDGROUND
        self.moved = False
        self.nearby_units = []
        self.observers = []
        self.rotate_tick = .1 #1 * pi/180.
        self.rotation = 0
        self.selectable = False
        self.selected = False
        self.selection_indicator = None
        self.selection_rotation = 0  

        # CONSTANTS
        self.CELL_SIZE = settings.CELL_SIZE
        self.ROTATION_RATE = 1 * pi/180 # radians = degrees * pi/180
        self.SELECTION_SCALE = 2
        self.SIZE = 30
        self.RADIUS = self.SIZE/2
        self.CLAUSTROPHOBIA = self.SIZE*2
        self.SPEED = 300.0 # pixels per frame
        self.UNBUNCH_SPEED = 40.0
        
    def move(self, dx, dy):
        c = self.CELL_SIZE
        self.current_quadrant = int(self.x/c), int(self.y/c)
        self.rotation = tan(dy/dx)
        
        self.x += dx
        self.y += dy
        
        self.new_quadrant = int(self.x/c), int(self.y/c)
        if self.current_quadrant != self.new_quadrant:
            self.notify("CHANGED CELL")
        
        #for s in self.graphics:
        #    transform_vertex_list(dx, dy, s)
        self.moved = True
        
    def select(self):
        if self.selectable and not self.is_selected():
            self.selected = True
            self.selection_indicator = st.SelectionTriangle(self)
            self.graphics.append(self.selection_indicator.graphic)
        
    def deselect(self):
        if self.is_selected():
            self.selected = False
        if self.selection_indicator:
            self.graphics.remove(self.selection_indicator.graphic)
            self.selection_indicator.graphic.delete()
            self.selection_indicator = None
            
    def is_selected(self):
        if self.selected:
            return True
        else:
            return False
        
        
    def get_nearby_units(self):
        self.nearby_units = find_units_in_circle((self.x, self.y), self.CLAUSTROPHOBIA*5, self.controller.all_units)
        for u in self.nearby_units:
            if u == self:
                self.nearby_units.remove(self)
        return self.nearby_units
        
    def receive_move_command(self, destination):
        self.current_command = self._walking
        self.current_destination = destination
        
    def receive_unbunch_command(self):
        self.current_command = self._unbunch
        
    def arrive(self):
        if self.get_nearby_units():
            self.receive_unbunch_command()
        else:
            self.current_command = None
        
    def _walking(self, dt):
        d_from_destination = get_distance((self.x, self.y), 
                                          (self.current_destination[0], self.current_destination[1])
                                          )
        if d_from_destination > 10:
            distance_traveled = self.SPEED * dt
            dx, dy = one_step_toward_destination(self.current_destination, 
                                                 (self.x, self.y), 
                                                 distance_traveled)
            self.move(dx, dy)
        else:
            self.arrive()
            self.current_destination = None
            
    def _unbunch(self, dt):
        closest_unit_distance = 1000
        closest_unit = None
        if self.nearby_units:
            for d in self.nearby_units:
                if get_distance((d.x, d.y), (self.x, self.y)) < closest_unit_distance:
                    closest_unit = d
                if get_distance((self.x, self.y), (d.x, d.y)) < self.CLAUSTROPHOBIA*5:
                    if self.current_command:
                        dx, dy = one_step_toward_destination((d.x, d.y), 
                                                             (self.x, self.y), 
                                                             (self.UNBUNCH_SPEED*dt))
                        self.move(-dx, -dy)
                        d.move(dx, dy)
            self.get_nearby_units()
        else:
            self.current_command = None
        

    def update(self, dt):
        self.moved = False
        if self.current_command:
            self.current_command(dt)
        if self.selection_indicator:
            self.selection_indicator.update(dt)
            
        x, y = self.x, self.y
        self.flat_poly.vertices = rotate_triangle((0, 0), self.RADIUS, self.rotation, (x, y))
        
        self.tick_selection_rotation()

    def tick_selection_rotation(self):
        self.selection_rotation += self.ROTATION_RATE

    def init_graphics(self):
        pass

    def add_observer(self, observer):
        self.observers.append(observer)
        self.CELL_SIZE = observer.CELL_SIZE
        
    def remove_observer(self, observer):
        self.observers.remove(observer)
        
    def notify(self, event):
        for o in self.observers:
            o.on_notify(self, event)