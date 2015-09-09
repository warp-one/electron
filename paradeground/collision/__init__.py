# # YOU'RE GONNA USE THE SEPARATING AXIS THEOREM
#
# http://www.metanetsoftware.com/technique/tutorialA.html
# http://www.metanetsoftware.com/
# http://www.sevenson.com.au/actionscript/sat/

import settings, grid

class CollisionManager(object):
    def __init__(self, unit_list, game_size):
        self.all_units = unit_list
        self.map_width = settings.MAP_WIDTH
        self.map_height = settings.MAP_HEIGHT
        self.grid = grid.Grid(self.map_width, self.map_height)
        
    def update(self, dt):
        pass