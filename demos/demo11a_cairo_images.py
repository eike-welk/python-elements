import sys
sys.path.insert(0, "..") # if Elements has yet to be installed

import elements
from elements.locals import *
import pygtk
pygtk.require('2.0')
import gtk
import cairo
import gobject
import time

# just found this, need to take a look:
#  ---> http://cairographics.org/threaded_animation_with_cairo/
# ----> http://www.tortall.net/mu/wiki/PyGTKCairoTutorial

#class myScreen(gtk.DrawingArea):
#    # Draw in response to an expose-event
#    __gsignals__ = { "expose-event": "override" }


# is there a possible problem with the timers and threading?
# i'm not exactly sure how these GTK timers work. could require some looking into.
# but i guess i won't worry about that for now since it doesn't seem like it's crashing *cough*
class myWindow(object):
    draw_poly = False
    points   = [] #
    mousex   = 0  #
    mousey   = 0  #
    fps_all  = [] # array of the "most recent fps" -- how long each draw call took
    fps_count=50  # how many samples to hold
    fps      =0   # the actual approximate fps
    def contact_add(self, c):
        #print "Any Contact"
        pass

    def contact_add_ball(self, c):
        print "Contact with Ball"

    def contact_add_poly(self, c):
        print "Polygon Contact"

    def destroy(self, widget, data=None):
        print "Quitting..."
        gtk.main_quit()

    def keydown(self, widget, event):
        keystr = gtk.gdk.keyval_name(event.keyval)
        if keystr == 'Escape':
            gtk.main_quit()
        #elif
        #else:
        #    print gtk.gdk.keyval_name(event.keyval)
    def keyup(self, widget, event):
        pass
        
    def mousemove(self, widget, event):
        self.mousex, self.mousey = event.x, event.y

        if self.draw_poly:
            pos = (event.x, event.y)
            self.points.append( pos )

    def mousedown(self, widget, event):
        pos = (event.x, event.y)
        print pos
        #return
        if event.button == 3:
            self.world.add.triangle(pos, sidelength=50)

        elif event.button == 1:
            # Start/Stop Wall-Drawing 
            if not self.draw_poly:
                self.draw_poly = True
                self.points = []
                self.points.append(pos)
        
    def mouseup(self, widget, event):
        self.mousex, self.mousey = event.x, event.y
        
        pos = (event.x, event.y) 

        if event.button == 1 and self.draw_poly:
            # Create Polygon
            self.draw_poly = False
            self.points.append(pos)
            if len(self.points) > 2: 
                body, self.points = self.world.add.complexPoly(self.points)
            else:
                self.world.add.rect(pos, width=80, height=30)
    
    def __init__(self, size = (640, 480)):
        print "Initializing the window..."
        # Create a new window
        self.window = win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        win.set_title("Demo 11 - Using GTK+/Cairo")
    
        # Connect the destroy function with the destruction of the window
        win.set_default_size(size[0], size[1])
 
        # Add the drawing area to the window
        da = gtk.DrawingArea()
        win.add(da)

        win.connect("destroy", self.destroy)

        win.connect("key_press_event", self.keydown)
        win.connect("key_release_event", self.keyup)

        da.set_events(gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK |
             gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK )
        da.connect("button_press_event", self.mousedown)
        da.connect("button_release_event", self.mouseup)
        win.connect("motion_notify_event", self.mousemove)

        # show the window 
        win.show_all()

        # Create the Physical Space Class
        self.world = world = elements.Elements(screen_size=size, renderer="cairo")
        #self.world.set_inputAxisOrigin(left=True, top=True)

        self.world.renderer.set_drawing_area(da)
        
        world.callbacks.add(CALLBACK_DRAWING_END, self.custom_draw)

        b1 = world.add.ball((211, 101), 50)
        b2 = world.add.ball((200, 100), 50)

        # Add contact callbacks    
        world.callbacks.add(CALLBACK_CONTACT_ADD, self.contact_add)
        world.callbacks.add(CALLBACK_CONTACT_ADD, self.contact_add_ball, [b1])
        
        # Add the ground
        world.add.ground()

        gobject.timeout_add(1000/60, self.physics_update)
        gobject.timeout_add(1000/60, self.draw_update)
        self.world.renderer.set_circle_image("smiley.png")
#        self.world.renderer.set_box_image("boxy.png")

    def custom_draw(self):
        r = self.world.renderer
        r.draw_circle((255,0,0), (self.mousex, self.mousey), 1)
        if self.points:
            r.draw_lines((1,0,0), False, self.points)
            for p in self.points:
                r.draw_circle((0.1,0.1,0.1), p, 5)
        r.draw_text("FPS: %d" % self.fps, center=(50,50))

    def physics_update(self):
        self.world.update()
        return True

    def draw_update(self):
        start = time.clock()
        
        ret = self.world.draw()

        elapsed = time.clock() - start
        if elapsed == 0: return ret
        
        self.fps_all.append(1 / elapsed)
        if len(self.fps_all) > self.fps_count:
            del self.fps_all[0]
            self.fps = 0
            for i in self.fps_all:
                self.fps += i
            self.fps /= self.fps_count

        return ret

    def main(self):
        gtk.main()

def create_test_images(filenames):
    pi = 3.14159
    w, h = 100, 100
    r    = w/2

    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    # svg writing:
    #sf = cairo.SVGSurface(file(filenames[0] + '.svg', "w"), w, h)
    c = cairo.Context(sf)

    # big yellow circle
    c.set_source_rgb(1,1,0.25)
    c.translate(w/2, h/2)
    c.arc(0, 0, r, 0, 2 * pi)
    c.fill()

    # mouth
    c.set_source_rgb(0,0,0)
    c.arc_negative(0, 0, w/4, 11.5/8 * 2 * pi, 8.5/8 * 2 * pi)
    c.stroke()

    # eyes
    c.arc(-w/8,-h/8, r/8, 0, 2 * pi)
    c.fill()
    c.arc( w/8,-h/8, r/8, 0, 2 * pi)
    c.fill()

    sf.write_to_png(filenames[0])
    # svg writing:
    #sf.finish()
    print "Wrote smiley to", filenames[0]

    w, h = 500, 100
    border = w/5

    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    c = cairo.Context(sf)

    # big yellow circle
    c.set_source_rgb(0,0,1)
    #c.translate(w/2, h/2)
    c.rectangle(0, 0, w, h)
    c.fill()

    c.set_source_rgba(1,1,1,0.5)
    c.rectangle(border, border, w-2*border, h-2*border)
    c.stroke()

    sf.write_to_png(filenames[1])
    print "Wrote test image to", filenames[1]

#    exit(0)

# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
    create_test_images( ["smiley.png", "boxy.png"])
    hello = myWindow()
    hello.main()

