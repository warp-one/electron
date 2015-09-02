import pyglet

BACKGROUND = pyglet.graphics.OrderedGroup(0)
MIDGROUND = pyglet.graphics.OrderedGroup(1)
FOREGROUND = pyglet.graphics.OrderedGroup(2)

FRAMERATE = 1/60.

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 800
CELL_SIZE = 150

ANTI_ALIASING = True

SCROLL_SPEED = FRAMERATE**(-1)/2

MAP_WIDTH = 2000
MAP_HEIGHT = 2000