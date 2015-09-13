import pyglet

import tools

class Grid(object):

    cell_size = 150

    def __init__(self, map_width, map_height):
        self.cells = []
        mapX = int(map_width/self.cell_size)+100
        mapY = int(map_height/self.cell_size)+100
        for c in range(mapX):
            self.cells.append([])
            for r in range(mapY):
                self.cells[c].append(None)
        self.collision = False
        
    def add(self, unit):
        cellX = int(unit.x/self.cell_size)
        cellY = int(unit.y/self.cell_size)

        unit.prev = None
        unit.next = self.cells[cellX][cellY]
        self.cells[cellX][cellY] = unit
        
        if unit.next != None:
            unit.next.prev = unit
            
    def get_units_in_cell(self, head):
        units_in_cell = set()
        while head != None:
            units_in_cell.add(head)
            head = head.next
        return units_in_cell
            
    def handle_cell(self, unit):
        # change to only walk over cells where a unit moved
        flagged_units = set()
        while unit != None:
            other_unit = unit.next
            while other_unit != None:
                # do anything that every unit in this cell needs to do with every other
                x1, y1 = unit.x + unit.dx, unit.y + unit.dy
                x2, y2 = other_unit.x + other_unit.dx, other_unit.y + other_unit.dy
                if tools.get_distance((x1, y1), (x2, y2)) < unit.RADIUS + other_unit.RADIUS:
                    flagged_units.update([unit, other_unit])
                other_unit = other_unit.next
            unit = unit.next
        return flagged_units
        
    def get_collision(self, unit, dx, dy):
        if self.collision:
            cellX, cellY = int(unit.x/self.cell_size), int(unit.y/self.cell_size)
            too_close_units = self.handle_cell(self.cells[cellX][cellY])
            if unit in too_close_units:
                return False
            else:
                return True
        else:
            return True
            
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
