from math import sqrt, pi, sin, cos

import pyglet

from tools import *
from selectiontriangle import SelectionTriangle
import settings


class BasicUnit(pyglet.sprite.Sprite):
    def __init__(self, controller, *args, **kwargs):
        super(BasicUnit, self).__init__(*args, **kwargs)
        
        self.controller = controller
        self.SIZE = 30
        self.SPEED = 300.0 # pixels per frame
        self.SHUFFLE_SPEED = 50.0
        self.RADIUS = self.SIZE/2
        self.graphics = []
        self.selected = False
        self.selectable = False
        self.current_command = None
        self.current_destination = None
        self.selection_indicator = None
        self.group = settings.FOREGROUND
        self.rotate_tick = .1 #1 * pi/180.
        self.nearby_units = []
        self.moved = False
        
        self.init_graphic()
        
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        for s in self.graphics:
            transform_vertex_list(dx, dy, s)
        self.moved = True
        
    def select(self):
        if self.selectable and not self.is_selected():
            self.selected = True
            self.selection_indicator = SelectionTriangle(self)
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
        
    def init_graphic(self):
        pass
        
    def get_nearby_units(self):
        self.nearby_units = find_units_in_circle((self.x, self.y), self.RADIUS, self.controller.all_units)
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
        if get_distance((self.x, self.y), (self.current_destination[0], self.current_destination[1])) > 10:
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
                if get_distance((self.x, self.y), (d.x, d.y)) < self.RADIUS:
                    if self.current_command:
                        dx, dy = one_step_toward_destination((d.x, d.y), (self.x, self.y), (self.SHUFFLE_SPEED*dt))
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
