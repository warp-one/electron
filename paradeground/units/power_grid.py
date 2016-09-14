from random import randint
from itertools import chain

import pyglet

from __init__ import BasicUnit, ThinkingUnit
from shape import Rectangle
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
    top_speed = 600.0
    acceleration = 20.0

    def __init__(self, *args, **kwargs):
        super(PowerGrid, self).__init__(*args, **kwargs)
        
        self.w, self.h = 300, 400
        self.init_graphics(strand_frequency=20)
        self.selectable = False
        self.points = []
        
    def create_grid_nodes(self, cell_size):
        for p in self.get_grid_points(cell_size):
            yield BasicUnit
        
        
    def calculate_colors_and_vertices(self, strand_frequency):
        self.num_strands = (self.w if self.w < self.h else self.h)/strand_frequency
        box_top_left = self.x - self.w/2, self.y + self.h/2
        box_bot_right = self.x + self.w/2, self.y - self.h/2
        if self.w < self.h:
            bot_vertices = [(box_bot_right[0] - strand_frequency*x, box_bot_right[1]) for x in range(self.num_strands)]
            top_vertices = [(box_top_left[0] + strand_frequency*x, box_top_left[1]) for x in range(self.num_strands)]
            top_vertices = top_vertices[::-1]
        else:
            bot_vertices = [(box_bot_right[0], box_bot_right[1] + strand_frequency*x) for x in range(self.num_strands)]
            top_vertices = [(box_top_left[0], box_top_left[1] - strand_frequency*x) for x in range(self.num_strands)]
            top_vertices = top_vertices[::-1]
        strand_vertices = []
        while bot_vertices or top_vertices:
            bv = bot_vertices.pop()
            tv = top_vertices.pop()
            strand_vertices.extend([bv, tv])
        self.strand_vertices = tuple([item for p in strand_vertices for item in p])

        
    def init_graphics(self, strand_frequency):
    
        self.calculate_colors_and_vertices(strand_frequency)
        self.strands = self.batch.add(len(self.strand_vertices)/2, pyglet.gl.GL_LINES, settings.MIDGROUND,
                                        ('v2f/stream', self.strand_vertices),
                                        ('c3B', tuple([randint(0, 255) for _ in range(len(self.strand_vertices)*3/2)]))
                                        )
        self.graphics.append(self.strands)
        
    def change_size(self, w, h, strand_frequency=20):
        self.strands.delete()
#        self.grid.re_grid(self)
        self.w, self.h = w, h
        self.init_graphics(strand_frequency)
        
    def update(self, dt):
#        if not self.points:
#            pts = self.get_grid_points(2000)
#            lenpts = len(pts)
#        
#            self.points = self.batch.add(lenpts, pyglet.gl.GL_POINTS, settings.FOREGROUND,
#                                        ('v2f/stream', tuple(chain(*pts))),
#                                        ('c3B', tuple([255]*3*lenpts))
#                                        )

        
        for s in self.statuses:
            self.statuses[s].update(dt)
        for i, p in enumerate(self.strands.vertices):
            if self.x != self.old_x or self.y != self.old_y:
                self.old_x, self.old_y = self.x, self.y
                self.change_size(self.w, self.h)
            if self.w < self.h:

                if not i%2:
                    x = self.strands.vertices[i] + randint(-1, 1)
                    if (x > self.x - self.w/2) and (x < self.x + self.w/2):
                                    
                        self.strands.vertices[i] = x
            else:
                if i%2:
                    x = self.strands.vertices[i] + randint(-1, 1)
                    if (x > self.y - self.h/2) and (x < self.y + self.h/2):
                                    
                        self.strands.vertices[i] = x
                    

                
        self.strands.colors = tuple([randint(0, 255) for _ in range(len(self.strand_vertices)*3/2)])
        #self.flat_poly.colors = list(get_rand_RGBs(lower=40)) + list(get_rand_RGBs(lower=180)) + list(get_rand_RGBs(lower=222))
        
    def handle_collision(self, collider):
        if collider.solid:
            try:
                collider.statuses["Speed"].trigger(self)
            except KeyError:
                print "Can't speed this unit up!"
        return False