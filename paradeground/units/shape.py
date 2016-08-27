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
