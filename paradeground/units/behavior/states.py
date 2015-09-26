import tools
from brain import State

class UnitStateWaiting(State):
    def __init__(self, unit):
        super(UnitStateWaiting, self).__init__("waiting")
        self.unit = unit
        
    def do_actions(self):
        pass
        
    def check_conditions(self):
        hostile_unit = self.unit.controller.get_close_entity(self.unit.get_location())
        ranging_distance = tools.get_distance(self.unit.leash_point, self.unit.get_location())
#        if hostile_unit:
#            if hostile_unit.team != self.unit.team:
#                self.unit.target = hostile_unit
#                print "gogo"
#                return "chasing"
                
        return None
        
    def entry_actions(self):
        print "now waiting"
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
            return "waiting"
        hostile_unit = self.unit.controller.get_close_entity(self.unit.get_location())
        if not hostile_unit:
            self.unit.target = None
            print "target lost"
            return "waiting"
                
        return None
        
    def entry_actions(self):
        print "now chasing"
        self.unit.leash_point = self.unit.get_location()
#        self.unit.receive_command(self.unit.target.get_location(), "MOVE")
        
class UnitStateMoveCommand(State):
    def __init__(self, unit):
        super(UnitStateMoveCommand, self).__init__("movecommand")
        self.unit = unit
        
    def get_distance_from_target(self):
        return tools.get_distance((self.unit.x, self.unit.y), 
                                  (self.unit.current_destination[0], self.unit.current_destination[1])
                                  )
        
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
            return "waiting"
                
        return None
        
    def entry_actions(self):
        print "now moving as ordered"
