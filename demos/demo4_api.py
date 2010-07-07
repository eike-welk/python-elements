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

def main():
    # PyGame Init
    pygame.init()
    size = (1200, 900)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    # Create the Physical Space Class
    world = elements.Elements(size)
    world.renderer.set_surface(screen)

    # Default Settings
    running = True

    # Main Loop
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                # Bye Bye
                running = False
                
            elif event.type == KEYDOWN and event.key == K_SPACE:    
                # Pause with SPACE
                world.run_physics = not world.run_physics

            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                # Add Ball
                world.add.ball(event.pos, radius=30, dynamic=False)
                
            elif event.type == MOUSEBUTTONDOWN and event.button == 3:
                # Add Square
                #world.add_triangle(event.pos, 60)
                world.add.rect(event.pos, width=100, height=20)
            
        # Clear Display
        screen.fill((255,255,255))

        # Update & Draw World
        world.update()
        world.draw()

        # Flip Display
        pygame.display.flip()
        
        # Try to stay at 50 FPS
        clock.tick(50)
        
        # output framerate in caption
        pygame.display.set_caption("elements: %i | fps: %i" % (world.element_count, int(clock.get_fps())))

if __name__ == "__main__":
    main()
