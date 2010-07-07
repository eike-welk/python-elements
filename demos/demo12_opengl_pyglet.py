"""
This file is an example for using 'Elements'
Elements is a 2D Physics API for Python using Box2D

Home:  http://elements.linuxuser.at
 IRC:  #elements on irc.freenode.net

Code:  svn co http://svn2.assembla.com/svn/elements          
       http://www.assembla.com/wiki/show/elements                  

License: Examples: Public Domain -- No legal restrictions
         Elements API: GPLv3
"""
from pyglet import window
from pyglet.gl import *

import sys
sys.path.insert(0, "..") # if Elements has yet to be installed

import elements
        
"""
  OpenGL Init Function
"""
def initGL():
    glClearColor(1.0, 1.0, 1.0, 0.0)

    glPointSize(3.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1000.0, 1000.0, -750.0, 750.0, -1.0, 1.0)
    glScalef(2.0, 2.0, 1.0)
    glMatrixMode(GL_MODELVIEW)

class Demo:
    def mouse_click(self, x, y, btn, d):
        if btn == 1:
            self.world.add.ball((x, y), radius=30)
        elif btn == 2:
            self.world.add.triangle((x, y), 40)
        else:
            self.world.add.rect((x, y), 20, 40)
            
        
    def main(self):
        # Window Size
        w, h = size = (900, 900)
    
        # OpenGL Init
        win = window.Window(w, h)        
        initGL()
    
        # Create the Physical Space Class
        self.world = elements.Elements(size, renderer='opengl_pyglet')
        
        # Set pyglet properties
        self.world.set_inputAxisOrigin(left=True, top=False)
        
        # Add ground
        self.world.add.ground()
        
        # Mouse click callback
        win.on_mouse_press = self.mouse_click
        
        # Main Loop
        while not win.has_exit:
            win.dispatch_events()
            win.clear()
    
            self.world.update()
            self.world.draw()
    
            win.flip()

if __name__ == "__main__":
    demo = Demo()
    demo.main()
