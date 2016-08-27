from random import randint

import pyglet

from __init__ import ThinkingUnit, Rectangle
import settings


def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = cycle(iter(it).next for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))



class PowerGrid(ThinkingUnit, Rectangle):

    solid = False
    shape = "rectangle"

    def __init__(self, *args, **kwargs):
        super(PowerGrid, self).__init__(*args, **kwargs)
        
        self.w, self.h = 600, 1600
        self.init_graphics()
        self.selectable = False
        
    def calculate_colors_and_vertices(self):
        strand_frequency = 5 # = width/num_strands
        self.num_strands = self.w/strand_frequency
        box_top = self.x - self.w/2, self.y + self.h/2
        box_bot = self.x - self.w/2, self.y - self.h/2
        bot_vertices = [(box_bot[0] + strand_frequency*x, box_bot[1]) for x in range(self.num_strands)]
        top_vertices = [(box_top[0] + strand_frequency*x, box_top[1]) for x in range(self.num_strands)]
        strand_vertices = []
        while bot_vertices or top_vertices:
            bv = bot_vertices.pop()
            tv = top_vertices.pop()
            strand_vertices.extend([bv, tv])
        self.strand_vertices = tuple([item for p in strand_vertices for item in p])

        
    def init_graphics(self):
    
        self.calculate_colors_and_vertices()
        self.strands = self.batch.add(len(self.strand_vertices)/2, pyglet.gl.GL_LINES, settings.MIDGROUND,
                                        ('v2f/stream', self.strand_vertices),
                                        ('c3B', tuple([randint(0, 255) for _ in range(len(self.strand_vertices)*3/2)]))
                                        )
        self.graphics.append(self.strands)
        
    def change_size(self, w, h):
        self.strands.delete()
        self.grid.re_grid(self)
        self.w, self.h = w, h
        self.init_graphics()
        
    def update(self, dt):
        
        for s in self.statuses:
            self.statuses[s].update(dt)
        for i, p in enumerate(self.strands.vertices):
            if self.x != self.old_x or self.y != self.old_y:
                self.old_x, self.old_y = self.x, self.y
                if i%2:
                    self.strands.vertices[i] += self.y - self.old_y
                else:
                    self.strands.vertices[i] += self.x - self.old_x

            if not i%2:
                x = self.strands.vertices[i] + randint(-1, 1)
                if (x > self.x - self.w/2) and (x < self.x + self.w/2):
                                
                    self.strands.vertices[i] = x
                    

                
        self.strands.colors = tuple([randint(0, 255) for _ in range(len(self.strand_vertices)*3/2)])
        #self.flat_poly.colors = list(get_rand_RGBs(lower=40)) + list(get_rand_RGBs(lower=180)) + list(get_rand_RGBs(lower=222))

    def not_collide(self, other):
        other.statuses["Speed"].deactivate()
        
    def handle_collision(self, collider):
        collider.statuses["Speed"].trigger()
        return False