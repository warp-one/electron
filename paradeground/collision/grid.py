class Grid(object):

    cell_size = 1500

    def __init__(self, map_width, map_height):
        self.cells = []
        columns = int(map_width/self.cell_size)
        rows = int(map_height/self.cell_size)
        for c in range(columns):
            self.cells.append([])
            for r in range(rows):
                self.cells[c].append(None)
        
    def add(self, unit):
        cellX = int(unit.x/self.cell_size)
        cellY = int(unit.y/self.cell_size)
        
        unit.prev = None
        unit.next = self.cells[cellX][cellY]
        self.cells[cellX][cellY] = unit
        
        if unit.next != None:
            unit.next.prev = unit
            
    def handle_collision(self, unit):
        # change to only walk over cells where a unit moved
        while unit != None:
            other_unit = unit.next
            while other_unit != None:
                if unit.x == other_unit.x and unit.y == other_unit.y:
                    pass # handle collision
                other_unit = other_unit.next
            unit = unit.next
            
    def move(self, unit, dx, dy):
        x, y = unit.x + dx, unit.y + dy
        old_cellX = int(unit.x/self.cell_size)
        old_cellY = int(unit.y/self.cell_size)
        
        cellX = int(x/self.cell_size)
        cellY = int(y/self.cell_size)
        
        unit.x = x
        unit.y = y
        
        if old_cellX == cellX and old_cellY == cellY:
            return
            
        if unit.prev != None:
            unit.prev.next = unit.next
            
        if unit.next != None:
            unit.next.prev = unit.prev
            
        if self.cells[old_cellX][old_cellY] == unit:
            self.cells[old_cellX][old_cellY] = unit.next
            
        self.add(unit)