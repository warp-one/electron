from random import randint

import pyglet

from unit import BasicUnit
from tools import transform_vertex_list

class Sparkle(BasicUnit):
    def __init__(self, *args, **kwargs):
        super(Sparkle, self).__init__(*args, **kwargs)
        
        self.selectable = True
        
        self.init_graphics()
        self.move(randint(100, 700), randint(100, 500))
        
    def init_graphics(self):
        num_spines = 1
        self.spines = []
        for _ in range(num_spines):
            self.spines.append(self.add_spine())
            
            
        self.graphics.extend(self.spines)

    def add_spine(self):
        x, y = self.x, self.y
        r = self.SIZE/2
        new_spine = self.batch.add(2, pyglet.gl.GL_LINES, self.group,
                                    ('v2f/stream', ((x - r), (y + r),
                                             (x + r), (y - r))),
                                    ('c3B', (255, 0, 255, 0, 255, 0))
                                   )
        return new_spine
