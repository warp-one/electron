from math import sqrt, pi, sin, cos, tan, degrees

import pyglet

from tools import *
from units.behavior import *
from units.behavior import states
from selection import selectiontriangle as st
import settings


class BasicUnit(pyglet.sprite.Sprite):

    ROTATION_RATE = 1 * pi/180 # radians = degrees * pi/180
    SELECTION_SCALE = 2
    SIZE = 32
    RADIUS = SIZE/2
    SPEED = 300.0 # pixels per frame

    def __init__(self, controller, grid, team=None, *args, **kwargs):
        super(BasicUnit, self).__init__(*args, **kwargs)
        
        self.team = team
        self.name = None
        self.id = 0
        
        self.controller = controller
        self.brain = StateMachine()
        self.leash_point = (0, 0)
        self.alert_range = 200
        self.target = None
        
        waiting_state = states.UnitStateWaiting(self)
        chasing_state = states.UnitStateChasing(self)
        command_state = states.UnitStateMoveCommand(self)
        
        self.brain.add_state(waiting_state)
        self.brain.add_state(chasing_state)
        self.brain.add_state(command_state)
        self.brain.set_state("waiting")
        
        # grid
        self.grid = grid
        self.prev = None
        self.next = None
        if self.grid:
            self.grid.add(self)
        
        self.current_destination = (0, 0)
        self.graphics = []
        self.group = settings.FOREGROUND
        self.sgroup = settings.MIDGROUND
        self.nearby_units = []
        self.rotate_tick = .1 #1 * pi/180.
        self.rotation = 0
        self.velocity = 0.
        self.selectable = False
        self.selected = False
        self.selection_indicator = None
        self.selection_rotation = 0  
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
            
    def stop(self):
        self.dx, self.dy = 0, 0
        
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
            
    def receive_command(self, target, command=None, origin=(0, 0)):
        if command == "MOVE":
            x = target[0] + self.x - origin[0]
            y = target[1] + self.y - origin[1]
            self.current_destination = (x, y)
            self.brain.set_state("movecommand")
        else:
            self.current_destination = target
            self.brain.set_state("movecommand")
        
    def arrive(self):
        self.current_destination = (0, 0)
        self.brain.set_state("waiting")
        self.stop()
        self.leash_point = self.get_location()
        
    def suicide(self):
        self.grid.remove(self)
        # u.spawn_death_animation()
        for g in self.graphics:
            g.delete()
        self.delete()
        
    def update(self, dt):
        self.velocity = self.SPEED * dt
        self.brain.think()
    
        if self.selection_indicator:
            self.selection_indicator.update(dt)
            
        x, y = self.x, self.y
        self.flat_poly.vertices = rotate_triangle((0, 0), self.RADIUS, self.rotation, (x, y))
        
        self.tick_selection_rotation()
        
    def get_location(self):
        return self.x, self.y

    def tick_selection_rotation(self):
        self.selection_rotation += self.ROTATION_RATE

    def init_graphics(self):
        pass