import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse

import settings
from selection import mouseselect as ms

def opengl_init():
    """ Initial OpenGL configuration.
    """
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDepthFunc(GL_LEQUAL)

def x_array(list):
    """ Converts a list to GLFloat list.
    """
    return (GLfloat * len(list))(*list)
    
class GameCamera(object):
    mode = 1
    x, y, z = 0, 0, 512
    rx, ry, rz = 0, 0, 0
    w, h = 640, 480
    far = 8192
    fov = 60
    
    def __init__(self):
        self.scrolling = False
        self.x_scroll, self.y_scroll = 0, 0
        

    def view(self, width, height):
        self.w, self.h = width, height
        glViewport(0, 0, width, height)
        if self.mode == 2:
            self.isometric()
        elif self.mode == 3:
            self.perspective()
        else:
            self.default()
            
    def adjust_xyz(self, dx, dy, dz):
        max_x = settings.MAP_WIDTH - settings.WINDOW_WIDTH
        min_x = 0
        max_y = settings.MAP_HEIGHT - settings.WINDOW_HEIGHT
        min_y = 0
        new_x = self.x + dx
        new_y = self.y + dy
        if new_x >= max_x:
            new_x = max_x
        elif new_x <= min_x:
            new_x = min_x
        else:
            self.x = new_x
        
        if new_y >= max_y:
            new_y = max_y
        elif new_y <= min_y:
            new_y = min_y
        else:
            self.y = new_y
            
        new_z = self.z + dz
        self.z = new_z
            
    def default(self):
        """ Default pyglet projection.
        """
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.w, 0, self.h, -1, self.far)
        glMatrixMode(GL_MODELVIEW)

    def isometric(self):
        """ Isometric projection.
        """
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-self.w/2., self.w/2., -self.h/2., self.h/2., 0, self.far)
        glMatrixMode(GL_MODELVIEW)

    def perspective(self):
        """ Perspective projection.
        """
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, float(self.w)/self.h, 0.1, self.far)
        glMatrixMode(GL_MODELVIEW)

    def key(self, symbol, modifiers):
        """ Key pressed event handler.
        """
        if symbol == key.F1:
            self.mode = 1
            self.default()
            print "Projection: Pyglet default"
        elif symbol == key.F2:
            print "Projection: 3D Isometric"
            self.mode = 2
            self.isometric()
        elif symbol == key.F3:
            print "Projection: 3D Perspective"
            self.mode = 3
            self.perspective()
        elif self.mode == 3 and symbol == key.NUM_SUBTRACT:
            self.fov -= 1
            self.perspective()
        elif self.mode == 3 and symbol == key.NUM_ADD:
            self.fov += 1
            self.perspective()
            
        else: print "KEY " + key.symbol_string(symbol)

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        """ Mouse drag event handler.
        """
        if button == 1:
            self.adjust_xyz(-dx*2, -dy*2, 0)
        elif button == 2:
            self.adjust_xyz(-dx*2, 0, -dz*2)
        elif button == 4:
            self.ry += dx/4.
            self.rx -= dy/4.
            
    def on_mouse_leave(self, x, y):
        self.x_scroll, self.y_scroll = 0, 0
        if x > settings.WINDOW_WIDTH:
            self.x_scroll = 1
        elif x < 0:
            self.x_scroll = -1
        if y > settings.WINDOW_HEIGHT:
            self.y_scroll = 1
        elif y < 0:
            self.y_scroll = -1
        self.scrolling = True
        
    def on_mouse_enter(self, x, y):
        self.x_scroll, self.y_scroll = 0, 0
        self.scrolling = False

    def apply(self):
        """ Apply camera transformation.
        """
        glLoadIdentity()
#        if self.mode == 1: return
        glTranslatef(-self.x, -self.y, -self.z)
        glRotatef(self.rx, 1, 0, 0)
        glRotatef(self.ry, 0, 1, 0)
        glRotatef(self.rz, 0, 0, 1)
        
    def scroll(self, dt):
        if self.scrolling:
            dx = settings.SCROLL_SPEED * self.x_scroll
            dy = settings.SCROLL_SPEED * self.y_scroll
            self.adjust_xyz(dx, dy, 0)
            
    def on_notify(self, unit, event):
        if event == "CENTER CAMERA":
            dx = unit.x - self.x - settings.WINDOW_WIDTH/2
            dy = unit.y - self.y - settings.WINDOW_HEIGHT/2
            self.adjust_xyz(dx, dy, 0)
            

class CameraWindow(pyglet.window.Window):
    def __init__(self):
        super(CameraWindow, self).__init__(resizable=True, 
                                           width=settings.WINDOW_WIDTH,
                                           height=settings.WINDOW_HEIGHT)
        opengl_init()
        self.cam = GameCamera()
        self.on_resize = self.cam.view
        self.on_key_press = self.cam.key
        #self.on_mouse_drag = self.cam.on_mouse_drag
        self.on_mouse_enter = self.cam.on_mouse_enter
        self.on_mouse_leave = self.cam.on_mouse_leave
        
        self.mouse_selector = ms.MouseSelector(self.cam)
        self.push_handlers(self.mouse_selector)
        
        pyglet.clock.schedule_interval(self.cam.scroll, settings.FRAMERATE)