import pyglet

import unit, settings, tools, resources

class StartTriangle(object):
    def __init__(self):
        self.vert1 = StartVertex(resources.mote, )
        
    def get_vertex_coordinates(self):
        self.x = settings.WINDOW_WIDTH/2
        self.y = settings.WINDOW_HEIGHT/2
        
        

class StartVertex(unit.BasicUnit):
    def __init__(self, *args, **kwargs):
        super(StartTriangle, self).__init__(*args, **kwargs)
        
    def init_graphics(self):
        self.graphics.extend(self.spines)

        x, y = self.x, self.y
        r = self.SIZE/2
        new_spine = self.batch.add(2, pyglet.gl.GL_POINTS, self.group,
                                    ('v2f/stream', (vertices),
                                    ('c3B', (255, 0, 255, 0, 255, 0))
                                   )
        return new_spine
