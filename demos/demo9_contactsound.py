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
import pygame
from pygame.locals import *
from pygame.color import *

from os import path
from sys import argv
from math import sqrt

import sys
sys.path.insert(0, "..") # if Elements has yet to be installed
import elements
from elements.locals import *

def load_sound(fullname):        
    if not pygame.mixer:#
        pygame.mixer.get_init()

    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message

    return sound

class Demo9:
    cur_sound = 0
    def __init__(self):
        # PyGame Init
        pygame.init()
        
        self.load_sounds()        
        self.clock = pygame.time.Clock()

        size = (1200, 900)
        self.screen = pygame.display.set_mode(size)

        self.world = elements.Elements(size)
        self.world.renderer.set_surface(self.screen)

    def load_sounds(self):
        self.snd = []
        for i in range(30): 
            #load to sound located at the same directory as this script
            s = load_sound(path.join(path.dirname(argv[0]),"beep.wav"))
            self.snd.append(s)

    def play_sound(self, vol=None):
        #the volume passed to this function cannot be negative
        #pygame takes care of the rest
        if vol != None:
            self.snd[self.cur_sound].set_volume(vol)
            print "volume: ", vol
        self.snd[self.cur_sound].play()

        self.cur_sound += 1
        if self.cur_sound == len(self.snd):
            self.cur_sound = 0
                        
    def contact_add(self, c):
        #the volume is calculated to be a fourth of the cubed root of the normal force on the body
        #thus, this can never be negative
        #volume = sqrt(c.normalForce) / 14
        volume = sqrt(c.velocity.Length()) / 14 # kne's hack since normalForce doesn't exist in 2.0.1
        self.play_sound(volume)
                    
    def run(self):
        b1 = self.world.add.ball((100, 100), 100)
    
        # Add Contact Callbacks    
        self.world.callbacks.add(CALLBACK_CONTACT_ADD, self.contact_add)
        
        # Add A Ground
        self.world.add.ground()
    
        # Default Settings
        running = True
        draw_poly = False
        points = []
        
        # Main Loop
        while running:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    # Bye Bye
                    running = False
                    
                elif event.type == KEYDOWN and event.key == K_SPACE:    
                    # Pause with SPACE
                    self.world.run_physics = not self.world.run_physics
                  
                elif event.type == MOUSEBUTTONDOWN and event.button == 3:
                    # Add Square
                    self.world.add.triangle(event.pos, sidelength=50)
    
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # Start/Stop Wall-Drawing 
                    #self.world.add_ball(event.pos)
                    if not draw_poly:
                        draw_poly = True
                        points = []
                        points.append(event.pos)
                        startpoly = True
                
                elif event.type == MOUSEBUTTONUP and event.button == 1:
                    if draw_poly:
                        # Create Polygon
                        draw_poly = False
                        points.append(event.pos)
                        if len(points) > 2: 
                            #print points
                            #print len(points)
                            body = self.world.add.complexPoly(points)
                            #self.world.add_callback(CALLBACK_CONTACT_ADD, contact_add_poly, body)
                        else:
                            self.world.add.rect(event.pos, width=80, height=30)
    
                elif event.type == MOUSEMOTION and draw_poly:
                    points.append(event.pos)

                    # Automatically release polygon if we get close the starting point
                    x1, y1 = points[0]
                    x2, y2 = event.pos
                    vx, vy = (x2-x1, y2-y1)
                    l = sqrt((vx*vx) + (vy*vy))
                    
                    if l < 20.0 and not startpoly:
                        d = { 'pos' : event.pos, 'button' : 1 }
                        pygame.event.post(pygame.event.Event(MOUSEBUTTONUP, d))
                        
                    elif l > 20.0 and startpoly:
                        startpoly = False
                
            # Clear Display
            self.screen.fill((255,255,255))
    
            # Update & Draw World
            self.world.update()
            self.world.draw()
    
            # Show line if drawing a wall
            if draw_poly and len(points) > 1:
                pygame.draw.lines(self.screen, (0,0,0), False, points)
    
            # Flip Display
            pygame.display.flip()
            
            # Try to stay at 50 FPS
            self.clock.tick(50)
            
            # output framerate in caption
            pygame.display.set_caption("elements: %i | fps: %i" % (self.world.element_count, int(self.clock.get_fps())))

if __name__ == "__main__":
    Game = Demo9()
    Game.run()
