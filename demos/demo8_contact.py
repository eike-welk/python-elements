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
    print "Any Contact"
#    print c
#    print c.normalForce
#    print c.tangentForce

def contact_add_ball(c):
    print "Contact with Ball"

def contact_add_poly(c):
    print "Polygon Contact"
        
def main():
    # PyGame Init
    pygame.init()
    size = (1200, 900)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    # Create the Physical Space Class
    world = elements.Elements(size)
    world.renderer.set_surface(screen)
    
    b1 = world.add.ball((100, 100), 100)

    # Add Contact Callbacks    
    world.callbacks.add(CALLBACK_CONTACT_ADD, contact_add)
    world.callbacks.add(CALLBACK_CONTACT_ADD, contact_add_ball, [b1])
    
    # Add A Ground
    world.add.ground()

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
                world.run_physics = not world.run_physics
              
            elif event.type == MOUSEBUTTONDOWN and event.button == 3:
                # Add Square
                world.add.triangle(event.pos, sidelength=50)

            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                # Start/Stop Wall-Drawing 
                #world.add_ball(event.pos)
                if not draw_poly:
                    draw_poly = True
                    points = []
                    points.append(event.pos)
            
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                if draw_poly:
                    # Create Polygon
                    draw_poly = False
                    points.append(event.pos)
                    if len(points) > 2: 
                        print points
                        print len(points)
                        body = world.add.complexPoly(points)
                        world.callbacks.add(CALLBACK_CONTACT_ADD, contact_add_poly, body)
                    else:
                        world.add.rect(event.pos, width=80, height=30)

            elif event.type == MOUSEMOTION and draw_poly:
                points.append(event.pos)

            
        # Clear Display
        screen.fill((255,255,255))

        # Update & Draw World
        world.update()
        world.draw()

        # Show line if drawing a wall
        if draw_poly and len(points) > 1:
            pygame.draw.lines(screen, THECOLORS["black"], False, points)

        # Flip Display
        pygame.display.flip()
        
        # Try to stay at 50 FPS
        clock.tick(50)
        
        # output framerate in caption
        pygame.display.set_caption("elements: %i | fps: %i" % (world.element_count, int(clock.get_fps())))

if __name__ == "__main__":
    main()
