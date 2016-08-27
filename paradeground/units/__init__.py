from math import sqrt, pi, sin, cos, tan, degrees
from random import randint

import pyglet

from tools import *
from units.behavior import *
from units.behavior import states
from selection import selectiontriangle as st
import settings

class Status(object):

    name = "Buff"


    def __init__(self, unit):
        self.unit = unit
        self.active = False
        
    def trigger(self):
        pass
        
    def update(self, dt):
        pass

class Speed(Status):

    name = "Speed"

    def __init__(self, unit, max_speed=600, acceleration=20):
        super(Speed, self).__init__(unit)
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.zones = set()
        
    def trigger(self, zone):
        self.zones.add(zone)
        
    def deactivate(self, zone):
        self.zones.discard(zone)
        
    def update(self, dt):
        speed_normal = (self.unit.current_speed - self.unit.BASE_SPEED)/(self.max_speed - self.unit.BASE_SPEED)
        if self.zones:
            if self.unit.current_speed < self.max_speed:
                self.unit.current_speed += min(self.acceleration, self.max_speed - self.unit.current_speed)
            if not randint(0, 270):
                self.unit.flat_poly.colors = [255 for x in self.unit.flat_poly.colors]
            self.unit.flat_poly.colors = [self.unit.color[i%3] + int((255 - x)*speed_normal) if not randint(0, 5) else self.unit.color[i%3] for i, x in enumerate(self.unit.flat_poly.colors)]

        else:
            if self.unit.current_speed > self.unit.BASE_SPEED:
                self.unit.current_speed -= min(self.acceleration, self.unit.current_speed - self.unit.BASE_SPEED)
            else:
                self.unit.flat_poly.colors = [int(self.unit.color[i%3]*.69) for i, x in enumerate(self.unit.flat_poly.colors)]
                


            
class BasicUnit(pyglet.sprite.Sprite):

    ROTATION_RATE = 1 * pi/180 # radians = degrees * pi/180
    selection_scale = 2
    size = 32
    radius = size/2
    BASE_SPEED = 300.0 # pixels per frame
    solid = True
    shape = "circle"

    def __init__(self, controller, grid, team=None, *args, **kwargs):
        super(BasicUnit, self).__init__(*args, **kwargs)
        
        self.controller = controller
        self.team = team
        self.name = None
        self.id = 0
        
        # grid
        self.grid = grid
        self.prev = None
        self.next = None
        if self.grid:
            self.grid.add(self)
        
        self.graphics = []
        self.group = settings.FOREGROUND
        self.sgroup = settings.MIDGROUND
        self.rotate_tick = .1 #1 * pi/180.
        self.rotation = 0
        self.velocity = 0.
        self.selectable = False
        self.selected = False
        self.selection_indicator = None
        self.selection_rotation = 0  
        
        self.current_speed = self.BASE_SPEED
        
        self.statuses = {}
        
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
        
    def suicide(self):
        self.grid.remove(self)
        #self.spawn_death_animation()
        for g in self.graphics:
            g.delete()
        self.delete()
        
    def update(self, dt):
        for s in self.statuses:
            self.statuses[s].update(dt)
        self.velocity = self.current_speed * dt
    
        if self.selection_indicator:
            self.selection_indicator.update(dt)
            
        x, y = self.x, self.y
        self.flat_poly.vertices = rotate_triangle((0, 0), self.radius, self.rotation, (x, y))
        
        self.tick_selection_rotation()
        
    def get_location(self):
        return self.x, self.y

    def tick_selection_rotation(self):
        self.selection_rotation += self.ROTATION_RATE

    def init_graphics(self):
        pass
        
    def handle_collision(self, collider):
        return self.solid
        
    def not_collide(self, other):
        pass
        

class ActiveUnit(BasicUnit):
    def __init__(self, *args, **kwargs):
        super(ActiveUnit, self).__init__(*args, **kwargs)
        
        self.current_destination = (0, 0)
        self.dx, self.dy = 0, 0
        self.old_x, self.old_y = 0, 0
        
    def move(self, dx, dy):
        self.dx, self.dy = dx, dy
        self.old_x, self.old_y = self.x, self.y
        
    def rotate(self, dx, dy):
        position = self.old_x, self.old_y
        mark = self.x + dx, self.y + dy
        heading = get_angle_in_radians(position, mark)
        self.rotation = heading
            
    def arrive(self):
        self.current_destination = (0, 0)
        self.brain.set_state("idleing")
        self.stop()
        self.leash_point = self.get_location()
        
    def stop(self):
        self.dx, self.dy = 0, 0
        
    def receive_command(self, target, command=None, origin=(0, 0)):
        if command == "MOVE":
            x = target[0] + self.x - origin[0]
            y = target[1] + self.y - origin[1]
            self.current_destination = (x, y)
            self.brain.set_state("movecommand")
        else:
            self.current_destination = target
            self.brain.set_state("movecommand")
        
    def update(self, dt):
        super(ActiveUnit, self).update(dt)
        
        
class ThinkingUnit(ActiveUnit):
    def __init__(self, *args, **kwargs):
        super(ThinkingUnit, self).__init__(*args, **kwargs)
        
        self.brain = StateMachine()
        self.leash_point = (0, 0)
        self.alert_range = 200
        self.target = None
        self.wait_count = 0
        
        idleing_state = states.UnitStateIdleing(self)
        chasing_state = states.UnitStateChasing(self)
        waiting_state = states.UnitStateWaiting(self)
        command_state = states.UnitStateMoveCommand(self)
        
        self.brain.add_state(idleing_state)
        self.brain.add_state(chasing_state)
        self.brain.add_state(waiting_state)
        self.brain.add_state(command_state)
        self.brain.set_state("idleing")
        

    def update(self, dt):
        super(ThinkingUnit, self).update(dt)
        self.brain.think()
        