import pyglet

BACKGROUND = pyglet.graphics.OrderedGroup(0)
MIDGROUND = pyglet.graphics.OrderedGroup(1)
FOREGROUND = pyglet.graphics.OrderedGroup(2)

FRAMERATE = 1/60.

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 800

ANTI_ALIASING = False

SCROLL_SPEED = FRAMERATE**(-1)/1.5

MAP_WIDTH = 2000
MAP_HEIGHT = 2000

PLAYER_COLOR = [50, 50, 255]
CPU1_COLOR = [255, 0, 0]