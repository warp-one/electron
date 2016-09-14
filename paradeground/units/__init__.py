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

    def __init__(self, unit, max_speed=600, acceleration=20, speed_bonus=30):
        super(Speed, self).__init__(unit)
        self.deceleration = acceleration
        self.max_speed = 600
        self.zones = set()
        self.speed_bonus = speed_bonus
        
    def trigger(self, zone):
        self.zones.add(zone)
        
    def deactivate(self, zone):
        return
        #self.zones.discard(zone)
        
    def update(self, dt):
        active = False
        if self.zones:
            max_speed = min([max([z.top_speed for z in self.zones]), self.unit.MAX_SPEED])
            acceleration = max([z.acceleration for z in self.zones])
            active = True
        else:
            max_speed = self.max_speed
        speed_normal = (self.unit.current_speed - self.unit.BASE_SPEED)/(max_speed - self.unit.BASE_SPEED)
        if active:
            if self.unit.current_speed < max_speed:
                self.unit.current_speed += min(acceleration, max_speed - self.unit.current_speed)
            self.unit.flat_poly.colors = [self.unit.color[i%3] + int((255 - x)*speed_normal) if not randint(0, 5) else self.unit.color[i%3] for i, x in enumerate(self.unit.flat_poly.colors)]

        else:
            if self.unit.current_speed > self.unit.BASE_SPEED:
                inactive_cap = max_speed - self.speed_bonus
                if self.unit.current_speed > inactive_cap:
                    self.unit.current_speed = inactive_cap
                else:
                    self.unit.current_speed -= min(self.deceleration/16, self.unit.current_speed - self.unit.BASE_SPEED)
                self.unit.flat_poly.colors = [self.unit.color[i%3] + int((255 - x)*speed_normal) if not randint(0, 5) else int(self.unit.color[i%3]) for i, x in enumerate(self.unit.flat_poly.colors)]
            else:
                self.unit.flat_poly.colors = [int(self.unit.color[i%3]*.69) for i, x in enumerate(self.unit.flat_poly.colors)]
        self.zones.clear()


            
class BasicUnit(pyglet.sprite.Sprite):

    ROTATION_RATE = 1 * pi/180 # radians = degrees * pi/180
    size = 32
    radius = size/2
    w = size
    h = size
    BASE_SPEED = 300.0 # pixels per frame
    MAX_SPEED = 600.0
    solid = True
    image_factor = 1
    selection_scale = 2 * image_factor
    immobile = False

    def __init__(self, team=None, *args, **kwargs):
        super(BasicUnit, self).__init__(*args, **kwargs)
        self.team = team
        self.name = None
        self.id = 0
        
        # grid
        self.prev = None
        self.next = None
        
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
        #self.spawn_death_animation()
        for g in self.graphics:
            g.delete()
        self.delete()
        
    def update(self, dt):
        self.rotation -= .01
        while self.rotation < 0:
            self.rotation += 360
        for s in self.statuses:
            self.statuses[s].update(dt)
        self.velocity = self.current_speed * dt
    
            
        
        self.tick_graphics(dt)
        
    def get_location(self):
        return self.x, self.y

    def tick_selection_rotation(self):
        self.selection_rotation += self.ROTATION_RATE

    def init_graphics(self):
        pass
        
    def tick_graphics(self, dt):
        if self.selection_indicator:
            self.selection_indicator.update(dt)
        self.tick_selection_rotation()
        
        
    def handle_collision(self, collider):
        return self.solid
        
        

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
#        heading = get_angle_in_radians(position, mark)
#        self.rotation = heading
            
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
        elif command == "STOP":
            self.current_destination = self.x, self.y
            self.stop()
            self.brain.set_state("idleing")
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
        