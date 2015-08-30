from math import sqrt

import pyglet

from tools import *
import settings, selectiontriangle

def get_equilateral_vertices(center, radius, rotation=0):
    x, y = center
    r = radius
    a = r/2
    triangle_side = 2*a*sqrt(3)
    bottom_left = x - triangle_side/2, y - a
    bottom_right = x + triangle_side/2, y - a
    top_center = x, y + r
    return (list(bottom_left) + list(bottom_right) + list(top_center))

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
        self.rotation = 0
        self.nearby_units = []
        
        self.init_graphic()
        
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        for s in self.graphics:
            transform_vertex_list(dx, dy, s)
        
    def select(self):
        if self.selectable:
            self.selected = True
        
            if not self.selection_indicator:
                self.selection_indicator = self.batch.add(3, pyglet.gl.GL_TRIANGLES, settings.MIDGROUND,
                    ('v2f/stream', get_equilateral_vertices((self.x, self.y), self.RADIUS)
        #            ('c3B', (0, 255, 0,
        #                     255, 0, 0,
        #                     0, 0, 255))
                   ))
                self.graphics.append(self.selection_indicator)
        
    def deselect(self):
        if self.is_selected:
            self.selected = False
        if self.selection_indicator:
            self.graphics.remove(self.selection_indicator)
            self.selection_indicator.delete()
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
                if self != d and get_distance((self.x, self.y), (d.x, d.y)) < self.RADIUS:
                    if not self.current_command and not d.current_command:
                        dx, dy = one_step_toward_destination((d.x, d.y), (self.x, self.y), (self.SHUFFLE_SPEED*dt))
                        self.move(-dx, -dy)
            self.get_nearby_units()
        else:
            self.current_command = None
        
    def update(self, dt):
        if self.current_command:
            self.current_command(dt)
        
        
