class Shape(object):
    shape = "oolou"

    @property
    def left(self):
        return self.x - self.w/2
    @property
    def right(self):
        return self.x + self.w/2
    @property
    def top(self):
        return self.y + self.h/2
    @property
    def bottom(self):
        return self.y - self.h/2
    @property
    def radius(self):
        return (self.w/2 if self.w > self.h else self.h/2)
        
    @property
    def corners(self):
        return self.x, self.y
        
    def get_grid_points(self, grid_cell_size):
        return [(self.x, self.y)]
                
class Rectangle(Shape):

    shape = "rectangle"

    @property
    def left(self):
        return self.x - self.w/2
    @property
    def right(self):
        return self.x + self.w/2
    @property
    def top(self):
        return self.y + self.h/2
    @property
    def bottom(self):
        return self.y - self.h/2
    @property
    def radius(self):
        return (self.w/2 if self.w > self.h else self.h/2)
    @property
    def corners(self):
        return self.left, self.right, self.top, self.bottom
        
    def get_grid_points(self, grid_cell_size):
        points = [(self.x, self.y)]
        points.extend([(self.left, self.top), (self.left, self.bottom),
                       (self.right, self.top), (self.right, self.bottom)])
        if grid_cell_size < .5*self.w:
            for x in range(self.w/grid_cell_size):
                points.append((self.left + x*grid_cell_size, self.top))
                points.append((self.left + x*grid_cell_size, self.bottom))
        if grid_cell_size < .5*self.h:
            for y in range(self.h/grid_cell_size):
            
                points.append((self.left, self.bottom + y*grid_cell_size))
                points.append((self.right, self.bottom + y*grid_cell_size))
        return points

        
class Circle(Shape):
    shape = "circle"

    @property
    def left(self):
        return self.x - self.radius
    @property
    def right(self):
        return self.x + self.radius
    @property
    def top(self):
        return self.y + self.radius
    @property
    def bottom(self):
        return self.y - self.radius
