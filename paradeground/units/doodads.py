import pyglet

import settings
from __init__ import BasicUnit

def combine_tuples(list_tuples):
    data = []
    for t in list_tuples:
        data.extend(list(t))
    return tuple(data)

class MapBorder(BasicUnit):
    def __init__(self, *args, **kwargs):
        super(MapBorder, self).__init__(*args, **kwargs)
        mw = settings.MAP_WIDTH
        mh = settings.MAP_HEIGHT
        bt = 100 # border thickness
        Lside = (0, 0, 0, mh, bt, 0, bt, mh)
        Rside = (mw - bt, 0, mw - bt, mh, mw, 0, mw, mh)
        Tside = (bt, 0, bt, bt, mw - bt, 0, mw - bt, bt)
        Bside = (bt, mh - bt, bt,  mh, mw - bt, mh - bt, mw - bt, mh)
        vertices = combine_tuples([Lside, Rside, Tside, Bside])
        self.border = self.batch.add_indexed(16, pyglet.gl.GL_TRIANGLES, self.group, 
                                             [0, 1, 2, 1, 2, 3, 
                                              4, 5, 6, 5, 6, 7, 
                                              8, 9, 10, 9, 10, 11, 
                                              12, 13, 14, 13, 14, 15], 
                                             ('v2f/static', vertices),
                                             ('c3B/static', tuple([50]*48))
                                             )

class Obstacle(BasicUnit):
    pass