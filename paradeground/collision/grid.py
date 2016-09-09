import pyglet

import tools, settings

def collides(unit, other):
    x1, y1 = unit.x + unit.dx, unit.y + unit.dy
    x2, y2 = other.x + other.dx, other.y + other.dy
    distance_old = tools.get_distance((unit.x, unit.y), (other.x, other.y))
    distance = tools.get_distance((x1, y1), (x2, y2))
    if unit.shape == "circle" and other.shape == "circle":
        if distance <= unit.radius + other.radius:
            return distance
        else:
            return False
    if unit.shape == "rectangle" and other.shape == "circle":
        if other.x > unit.left and other.x < unit.right:
            if other.y > unit.bottom and other.y < unit.top:
                return True
        else:
            return False
    if unit.shape == "circle" and other.shape == "rectangle":
        if unit.x > other.left and unit.x < other.right:
            if unit.y > other.bottom and unit.y < other.top:
                return True
        else:
            return False
        


class Grid(object):

    cell_size = 2000

    def __init__(self, map_width, map_height):
        self.cells = []
        self.map_width = map_width
        self.map_height = map_height
        self.mapX = int(map_width/self.cell_size)
        self.mapY = int(map_height/self.cell_size)
        for c in range(self.mapX):
            self.cells.append([])
            for r in range(self.mapY):
                self.cells[c].append(None)
        self.collision = False
        self.colliding_units = set()
        
    def add(self, unit):
        for c in self.get_cell_numbers(unit):
            cellX, cellY = c
            unit.prev = None
            unit.next = self.cells[cellX][cellY]
            self.cells[cellX][cellY] = unit
            
            if unit.next != None:
                unit.next.prev = unit
            
    def remove(self, unit):
        for c in self.get_cell_numbers(unit):
            cellX, cellY = c
        
            if unit.prev != None:
                unit.prev.next = unit.next
            if unit.next != None:
                unit.next.prev = unit.prev
            
            if self.cells[cellX][cellY] == unit:
                self.cells[cellX][cellY] = unit.next

    def get_cell_numbers(self, unit):
        cells = set()
        cells.add((int(unit.x/self.cell_size), int(unit.y/self.cell_size)))
#        if self.cell_size < unit.radius:
        grid_points = unit.get_grid_points(self.cell_size)
        for c in grid_points:
            if c[0] > self.mapX or c[1] > self.mapY:
                continue
            cells.add((int(c[0]/self.cell_size), int(c[1]/self.cell_size)))
#        else:
#            cells.append((int(unit.x/self.cell_size), int(unit.y/self.cell_size)))
        return cells
            
    def get_units_in_cell(self, head):
        units_in_cell = set()
        while head != None:
            units_in_cell.add(head)
            head = head.next
        return units_in_cell
        
    def handle_cell(self, cellX, cellY):
        # IF YOU change to only walk over cells where a unit moved
        # it will break zones
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
            if cellX > 0 and cellY < self.mapY - 1:
                flagged_units.update(self.handle_unit(unit, self.cells[cellX-1][cellY+1]))
                #########
#            if cellX < self.mapX - 1 and cellY < self.mapY - 1:
#                flagged_units.update(self.handle_unit(unit, self.cells[cellX+1][cellY+1]))
#            if cellX < self.mapX - 1:
#                flagged_units.update(self.handle_unit(unit, self.cells[cellX+1][cellY]))
#            if cellY < self.mapY - 1:
#                flagged_units.update(self.handle_unit(unit, self.cells[cellX][cellY+1]))
#            if cellX < self.mapX - 1 and cellY > 0:
#                flagged_units.update(self.handle_unit(unit, self.cells[cellX+1][cellY-1]))
                

            unit = unit.next
        return flagged_units
        
    def handle_unit(self, unit, other):
        flagged = set()
        adjusts = set()
        while other != None:
            proximity = collides(unit, other)
            if proximity:
                unit_collided = unit.handle_collision(other)
                other_collided = other.handle_collision(unit)
                if unit_collided and other_collided:
                    flagged.update([unit, other])
                    

                    if unit.solid and other.solid:
                        if proximity < unit.radius + other.radius:
                            dx, dy = tools.one_step_toward_destination((other.x, other.y), 
                                             (unit.x, unit.y), 
                                             (40./6))
                                             
                                             
                            self.move(unit, -dx, -dy)
                            self.move(other, dx, dy)
                            unit.brain.set_state("waiting")
                            other.brain.set_state("waiting")
                            adjusts.update([unit, other])

            else:
                pass
            other = other.next
        flagged.difference_update(adjusts)
        return flagged
        
    def re_grid(self, unit):
        self.remove(unit)
        self.add(unit)
        
    def move(self, unit, dx, dy):
        if not dx and not dy:
            return
        x, y = unit.x + dx, unit.y + dy
        if x > settings.MAP_WIDTH:
            x = settings.MAP_WIDTH - 1
        if y > settings.MAP_HEIGHT:
            y = settings.MAP_HEIGHT - 1
        old_cellX = int(unit.x/self.cell_size)
        old_cellY = int(unit.y/self.cell_size)
        
        cellX = int(x/self.cell_size)
        cellY = int(y/self.cell_size)
        
        unit.x = x
        unit.y = y
#        unit.rotate(dx, dy)
        
        if old_cellX == cellX and old_cellY == cellY:
            return
            
        if unit.prev != None:
            unit.prev.next = unit.next
            
        if unit.next != None:
            unit.next.prev = unit.prev
        
        try:
            if self.cells[old_cellX][old_cellY] == unit:
                self.cells[old_cellX][old_cellY] = unit.next
        except IndexError:
            print unit, old_cellX, old_cellY
            
        try:
            self.add(unit)
        except IndexError:
            print unit
        unit.stop()
        
    def update(self, dt):
        self.colliding_units.clear()
        for r in self.cells:
            for u in r:
                if u:
                    cells = self.get_cell_numbers(u)
                    for c in cells:
                        self.colliding_units.update(self.handle_cell(c[0], c[1]))