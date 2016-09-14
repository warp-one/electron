import tools
from brain import State

class UnitStateIdleing(State):
    def __init__(self, unit):
        super(UnitStateIdleing, self).__init__("idleing")
        self.unit = unit
        
    def do_actions(self):
        pass
        
    def check_conditions(self):
#        hostile_unit = self.unit.controller.get_close_entity(self.unit.get_location())
#        ranging_distance = tools.get_distance(self.unit.leash_point, self.unit.get_location())
#        if hostile_unit:
#            if hostile_unit.team != self.unit.team:
#                self.unit.target = hostile_unit
#                print "gogo"
#                return "chasing"
                
        return None
        
    def entry_actions(self):
        self.unit.wait_time = 0
        self.unit.current_destination = self.unit.get_location()
        print "now idleing"
#        self.unit.receive_command(self.unit.leash_point, "MOVE")

        
class UnitStateChasing(State):
    def __init__(self, unit):
        super(UnitStateChasing, self).__init__("chasing")
        self.unit = unit
        
    def do_actions(self):
        print "asgasgagafdgadfgASGAGAFGADFG"
        self.unit.current_destination = self.unit.target.get_location()
        
    def check_conditions(self):
        ranging_distance = tools.get_distance(self.unit.leash_point, self.unit.get_location())
        if ranging_distance > self.unit.alert_range:
            print "too far!"
            self.unit.current_destination = self.unit.leash_point
            return "movecommand"
#        hostile_unit = self.unit.controller.get_close_entity(self.unit.get_location())
#        if not hostile_unit:
#            self.unit.target = None
#            print "target lost"
#            return "idleing"
                
        return None
        
    def entry_actions(self):
        print "now chasing"
        self.unit.leash_point = self.unit.get_location()
        self.unit.receive_command(self.unit.target.get_location(), "MOVE")

        
class UnitStateWaiting(State):
    def __init__(self, unit):
        super(UnitStateWaiting, self).__init__("waiting")
        self.unit = unit
        self.idle_time = 0
        self.waiting_period = 10 #in game ticks
        
    def do_actions(self):
        self.idle_time += 1

    def check_conditions(self):
        if tools.get_distance(self.unit.current_destination, self.unit.get_location()) < self.unit.radius*4:
            return "idleing"
        if self.idle_time >= self.waiting_period:
            print "trying again"
            return "movecommand"
                
        return None
        
    def entry_actions(self):
        self.unit.wait_count += 1
        self.unit.dx, self.unit.dy = 0, 0
        self.idle_time = 0
        print "waiting... for the " + str(self.unit.wait_count) + "th time"

        
class UnitStateMoveCommand(State):
    def __init__(self, unit):
        super(UnitStateMoveCommand, self).__init__("movecommand")
        self.unit = unit
        
    def do_actions(self):
        distance_traveled = self.unit.velocity
        dx, dy = tools.one_step_toward_destination(self.unit.current_destination, 
                                             (self.unit.x, self.unit.y), 
                                             distance_traveled)
        self.unit.move(dx, dy)

    def check_conditions(self):
        if self.get_distance_from_target() < 10:
            self.unit.arrive()
            print "made it!"
            return "idleing"
        if self.unit.wait_time > 3:
            return "idleing"
                
        return None
        
    def entry_actions(self):
        print "now moving as ordered"

