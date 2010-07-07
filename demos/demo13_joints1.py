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

import sys
sys.path.insert(0, "..") # if Elements has yet to be installed

import elements
from elements.locals import *

def contact_add(c):
    #print "Any Contact"
    pass
#    print c
#    print c.normalForce
#    print c.tangentForce

def contact_add_ball(c):
    print "Contact with Ball"

def contact_add_poly(c):
    print "Polygon Contact"
    
def main():
    print "(i) Draw a line between two bodies to create a distance joint"

    # PyGame Init
    pygame.init()
    size = (1200, 900)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    # Create the Physical Space Class
    world = elements.Elements(size)
    world.renderer.set_surface(screen)
    
    # Add A Ground
    world.add.ground()

    # Joint 1:
    # Fix a Rectangle to the Background with a Revolute Joint in the center
    body = world.add.rect((440, 200), width=160, height=20)
    world.add.joint(body)
    
    # Default Settings
    running = True
    draw_poly = False
    points = []
    p2 = []
    p3 = []
    
    # Joint Bodies
    jb1 = None
    jb2 = None
        
    # Main Loop
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                # Bye Bye
                running = False
                
            elif event.type == KEYDOWN and event.key == K_SPACE:    
                # Pause with SPACE
                world.run_physics = not world.run_physics
              
            elif event.type == MOUSEBUTTONDOWN and event.button == 3:
                # Add Square
                world.add.triangle(event.pos, sidelength=50)

            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                jb1 = jb2 = None # Joint Bodies
                jb1 = world.get_bodies_at_pos(event.pos)
                
                if not draw_poly:
                    draw_poly = True
                    points = []
                    points.append(event.pos)
            
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                if jb1:
                    jb2 = world.get_bodies_at_pos(event.pos)
                    
                    if jb2:
                        if str(jb1) != str(jb2):
                            print jb1, jb2
                            print "add joint"
                            world.add.joint(jb1[0], jb2[0], points[0], points[-1])
                            draw_poly = False
                            continue 
                                            
                if draw_poly:
                    # Create Polygon
                    draw_poly = False
                    points.append(event.pos)
                    if len(points) > 2: 
                        #print points
                        #print len(points)
                        body, p2 = world.add.complexPoly(points)
                        
                    else:
                        world.add.rect(event.pos, width=70, height=20)
                        
            elif event.type == MOUSEMOTION and draw_poly:
                world.run_physics = False
                points.append(event.pos)
            
        # Clear Display
        screen.fill((255,255,255))

        # Update & Draw World
        world.update()
        world.draw()

        # Show line if drawing a wall
        if draw_poly and len(points) > 1:
            #print points
            world.renderer.draw_lines(THECOLORS["black"], False, points, 3)
        
        # Draw polygon reduced spots and line
        if p2 != None and len(p2) > 2:
            world.renderer.draw_lines(THECOLORS["red"], False, p2, 2)
            for p in p2:
                world.renderer.draw_circle(THECOLORS["red"], p, 5, 0)
        
        # Flip Display
        pygame.display.flip()
        
        # Try to stay at 50 FPS
        clock.tick(50)
        
        # output framerate in caption
        pygame.display.set_caption("elements: %i | fps: %i" % (world.element_count, int(clock.get_fps())))

if __name__ == "__main__":
    main()
