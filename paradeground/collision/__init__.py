import settings

class CollisionManager(object):
    def __init__(self, unit_list, game_size):
        self.all_units = unit_list
        self.map_width = settings.MAP_WIDTH
        self.map_height = settings.MAP_HEIGHT
        self.grid_cells = []
    
        self.CELL_SIZE = 150
        
    def create_grid(self):
        self.grid_columns = int(self.map_width / self.CELL_SIZE) + 1
        self.grid_rows = int(self.map_height / self.CELL_SIZE) + 1
        for _ in range(self.grid_columns*self.grid_rows):
            self.grid_cells.append([])
        
        
    def distribute_units(self):
        for u in self.all_units:
            u.add_observer(self)
            u.CELL_SIZE = self.CELL_SIZE
            self.sort_unit(u)
            
    def move_unit(self, unit):
        self.remove_unit(unit)
        self.sort_unit(unit)
            
    def remove_unit(self, unit):
        i = self.get_cell_index_from_coord(unit.current_quadrant)
        self.grid_cells[i].remove(unit)
        
    def sort_unit(self, unit):
        i = self.get_cell_index_from_coord(unit.new_quadrant)
        self.grid_cells[i].append(unit)
        
    def check_collision_in_cell(self, cell):
        pass
        
    def on_notify(self, unit, event):
        if event == "CHANGED CELL":
            self.move_unit(unit)
            
    def get_cell_index_from_coord(self, coord):
        return int(coord[0]) + int(coord[1]*self.grid_columns)
        
    def get_coord_from_cell_index(self, index):
        return index%self.grid_columns - 1, index/self.grid_columns - 1

    def create_debug_labels(self):
        self.debug_labels = []
        for c in self.grid_cells:
            pass
        
    def debug(self):
        for i, c in enumerate(self.grid_cells):
            pass
            
    