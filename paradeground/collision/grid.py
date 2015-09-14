import pyglet

import tools

class Grid(object):

    cell_size = 150

    def __init__(self, map_width, map_height):
        self.cells = []
        mapX = int(map_width/self.cell_size)
        mapY = int(map_height/self.cell_size)
        for c in range(mapX):
            self.cells.append([])
            for r in range(mapY):
                self.cells[c].append(None)
        self.collision = False
        self.colliding_units = set()
        
    def add(self, unit):
        cellX = int(unit.x/self.cell_size)
        cellY = int(unit.y/self.cell_size)

        unit.prev = None
        unit.next = self.cells[cellX][cellY]
        self.cells[cellX][cellY] = unit
        
        if unit.next != None:
            unit.next.prev = unit
            
    def get_cell_number(self, unit):
        return int(unit.x/self.cell_size), int(unit.y/self.cell_size)
            
    def get_units_in_cell(self, head):
        units_in_cell = set()
        while head != None:
            units_in_cell.add(head)
            head = head.next
        return units_in_cell
        
    def handle_cell(self, cellX, cellY):
        # change to only walk over cells where a unit moved
        unit = self.cells[cellX][cellY]
        flagged_units = set()
        while unit != None:
            flagged_units.update(self.handle_unit(unit, unit.next))
            if cellX > 0 and cellY > 0:
                flagged_units.update(self.handle_unit(unit, self.cells[cellX-1][cellY-1]))
            if cellX > 0:
                flagged_units.update(self.handle_unit(unit, self.cells[cellX-1][cellY]))
            if cellY > 0:
                flagged_units.update(self.handle_unit(unit, self.cells[cellX][cellY-1]))
            if cellX > 0 and cellY < len(self.cells[0]) - 1:
                flagged_units.update(self.handle_unit(unit, self.cells[cellX-1][cellY+1]))

            unit = unit.next
        return flagged_units
        
    def handle_unit(self, unit, other):
        flagged = set()
        while other != None:
            x1, y1 = unit.x + unit.dx, unit.y + unit.dy
            x2, y2 = other.x + other.dx, other.y + other.dy
            distance = tools.get_distance((x1, y1), (x2, y2))
            if distance <= unit.RADIUS + other.RADIUS:
                flagged.update([unit, other])
                if distance < unit.RADIUS + other.RADIUS:
                    dx, dy = tools.one_step_toward_destination((other.x, other.y), 
                                     (unit.x, unit.y), 
                                     (10./6))
                    self.move(unit, -dx, -dy)
                    self.move(other, dx, dy)
                    unit.arrive()
                    other.arrive()

            other = other.next
        return flagged
        
    def get_collision(self, unit, dx, dy):
        if self.collision:
            cellX, cellY = int(unit.x/self.cell_size), int(unit.y/self.cell_size)
            too_close_units = self.handle_cell(cellX, cellY)
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
        unit.dx, unit.dy = 0, 0
        
    def update(self, dt):
        self.colliding_units.clear()
        for r in self.cells:
            for u in r:
                if u:
                    cell = self.get_cell_number(u)
                    self.colliding_units.update(self.handle_cell(cell[0], cell[1]))
