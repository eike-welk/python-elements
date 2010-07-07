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
    size = (800, 800)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
        
    # Create the Physical Space Class
    world = elements.Elements(size)
    world.renderer.set_surface(screen)

    # Add A Ground
    world.add.ground()
    world.add.wall((100, 100), (300, 300), 5)
    
    # Default Settings
    running = True
    
    a = 0

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
                # Add Mouse Joint if at an Object
                bodylist = world.get_bodies_at_pos(event.pos, include_static=False)
                print bodylist
                if bodylist and len(bodylist) > 0:
                    world.add.mouseJoint(bodylist[0], event.pos)
            
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                # Delete Mouse Joint
                world.add.remove_mouseJoint()

            elif event.type == MOUSEMOTION and event.buttons[0]:
                world.mouse_move(event.pos)
                
            elif event.type == MOUSEBUTTONDOWN and event.button == 3:
                # Add Square
                world.add.rect(event.pos, width=40, height=20, angle=a)
                a += 10

            elif event.type == KEYDOWN:
                if event.unicode == "1":
                    # Add many Balls
                    x, y = pygame.mouse.get_pos()
                    for i in range(5):
                        for j in range(5): world.add.ball((x-i,y-j), radius=20)

                elif event.unicode == "2":
                    # Add many Balls
                    x, y = pygame.mouse.get_pos()
                    for i in range(5):
                        for j in range(5): world.add.rect((x-i,y-j), width=40, height=20, angle=a)
            
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
