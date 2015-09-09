# # YOU'RE GONNA USE THE SEPARATING AXIS THEOREM
#
# http://www.metanetsoftware.com/technique/tutorialA.html
# http://www.metanetsoftware.com/
# http://www.sevenson.com.au/actionscript/sat/

import settings

class CollisionManager(object):
    def __init__(self, unit_list, game_size):
        self.all_units = unit_list
        self.map_width = settings.MAP_WIDTH
        self.map_height = settings.MAP_HEIGHT
        self.grid_cells = []
        self.cell_index_to_run_collision = set()
    
        self.CELL_SIZE = 15000
        
    def create_grid(self):
        self.grid_columns = int(self.map_width / self.CELL_SIZE) + 1
        self.grid_rows = int(self.map_height / self.CELL_SIZE) + 1
        for _ in range(self.grid_columns*self.grid_rows):
            self.grid_cells.append([])
        
        
    def distribute_units(self, unit_list):
        for u in unit_list:
            u.add_observer(self)
            
    def move_unit(self, unit):
        self.remove_unit(unit)
        self.sort_unit(unit)
            
    def remove_unit(self, unit):
        unit_quadrant = self.get_cell_coord(unit.old_x, unit.old_y)
        i = self.get_cell_index_from_coord(unit_quadrant)
        if unit in self.grid_cells[i]:
            print "removing"
            self.grid_cells[i].remove(unit)
        
    def sort_unit(self, unit):
        unit_quadrant = self.get_cell_coord(unit.x, unit.y)
        i = self.get_cell_index_from_coord(unit_quadrant)
        self.grid_cells[i].append(unit)
        
    def check_collision_in_cell(self, cell):
        unblocked_units = []
        for u in self.grid_cells[cell]:
            unblocked_units.append(u)
        return unblocked_units
        
    def flag_cell_for_collision(self, unit_cell):
        self.cell_index_to_run_collision.add(unit_cell)
        
    def on_notify(self, unit, event):
        if event == "MOVE":
            cell_coordinate = self.get_cell_coord(unit.old_x, unit.old_y)
            
            unit_cell = self.get_cell_index_from_coord(cell_coordinate)
            if unit_cell not in self.cell_index_to_run_collision:
                self.flag_cell_for_collision(unit_cell)
                
    def get_cell_coord(self, x, y):
        return int(x/self.CELL_SIZE), int(y/self.CELL_SIZE)
            
    def get_cell_index_from_coord(self, coord):
        return int(coord[0]) + int(coord[1]*self.grid_columns)
        
    def get_coord_from_cell_index(self, index):
        return index%self.grid_columns - 1, index/self.grid_columns - 1

    def update(self, dt):
        unblocked_units = []
        for cell in self.cell_index_to_run_collision:
            unblocked_units.extend(self.check_collision_in_cell(cell))
        print len(unblocked_units)
        for u in unblocked_units:
            u.proceed()
            old_cell = self.get_cell_coord(u.old_x, u.old_y)
            new_cell = self.get_cell_coord(u.new_x, u.new_y)
            if old_cell != new_cell:
                self.move_unit(u)
        self.cell_index_to_run_collision.clear()