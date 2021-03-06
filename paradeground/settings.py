import pyglet

BACKGROUND = pyglet.graphics.OrderedGroup(0)
MIDGROUND = pyglet.graphics.OrderedGroup(1)
FOREGROUND = pyglet.graphics.OrderedGroup(2)

FRAMERATE = 1/60.

WINDOW_WIDTH = 1680
WINDOW_HEIGHT = 1050

ANTI_ALIASING = True

SCROLL_SPEED = FRAMERATE**(-1)/1.5

MAP_WIDTH = 3000
MAP_HEIGHT = 3000

PLAYER_COLOR = [50, 50, 255]
CPU1_COLOR = [255, 0, 0]