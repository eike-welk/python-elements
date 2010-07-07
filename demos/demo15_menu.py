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

from sys import exit
from os.path import isfile

import sys
sys.path.insert(0, "..") # if Elements has yet to be installed

import elements
from elements.locals import *
from elements.menu import *
    
def click_menu(*args):
    print "Menu Click:", args
    if args[0] == "Quit": 
        exit(0)
    
    elif args[0] == "Pause":
        args[1].run_physics = not args[1].run_physics
        
    elif args[0] == "Screenshot":
        world = args[1]

        # Create an empty surface
        s = pygame.Surface((world.display_width, world.display_height))
        s.fill((255,255,255))
        
        # Draw the physics on the temporary surface and change back to the old surface
        s_old = world.renderer.get_surface()
        world.renderer.set_surface(s)
        world.draw()
        world.renderer.set_surface(s_old)

        # Create Filename
        fn = "screenshot"
        i = 1
        while isfile("%s%i.tga" % (fn, i)): 
            i += 1
            
        # Save Image
        pygame.image.save(s, "%s%i.tga" % (fn, i))
        print "Screenshot saved as: %s%i.tga" % (fn, i)
        
def main():    
    # PyGame Init
    pygame.init()
    size = (1200, 900)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    # Create the Physical Space Class
    world = elements.Elements(size)
    world.renderer.set_surface(screen)

    menu = MenuClass()
    
    # Add Main Menu Items
    item1 = menu.addItem('File', callback=click_menu)
    item2 = menu.addItem('Item2')

    # Add SubMenu Items (parent=...)
    # 1. For [File] (parent=item1)
    menu.addItem('Pause', callback=click_menu, parent=item1, userData=world)
    menu.addItem('Screenshot', callback=click_menu, parent=item1, userData=world)
    menu.addItem('Quit', callback=click_menu, parent=item1)
    
    # 2. For [Item2] (parent=item2)
    menu.addItem('SubItem', callback=click_menu, parent=item2)
    menu.addItem('SubItem2', callback=click_menu, parent=item2)
    
    # Add A Ground
    world.add.ground()

    # Joint 1:
    # Fix a Rectangle to the Background with a Revolute Joint in the center
    body = world.add.rect((140, 700), width=160, height=20)
    world.add.joint(body)
    
    body = world.add.rect((640, 100), width=320, height=20)
    world.add.joint(body)    
    
    # Start at x,y=(100,100), means 100 pixels to the right and 100 pixels down
    #world.camera.set_offset((100, 100))
    
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
                
            elif event.type == KEYDOWN:
                #print event.key
                if event.key == K_SPACE:    
                    # Pause with SPACE
                    world.run_physics = not world.run_physics

                elif event.unicode == "+":
                    world.camera.inc_scale_factor(+0.1)

                elif event.unicode == "-":
                    world.camera.inc_scale_factor(-0.1)
              
                elif event.key in [271, 13]:
                    pygame.event.post(pygame.event.Event(MOUSEBUTTONUP, { 'button': 2, 'pos' : pygame.mouse.get_pos() }))
                    
                elif event.key == 273: # up
                    world.camera.inc_offset((0, -30))
                    
                elif event.key == 274: # down
                    world.camera.inc_offset((0, 30))
                    
                elif event.key == 276: # left
                    world.camera.inc_offset((-30, 0))
                    
                elif event.key == 275: # right
                    world.camera.inc_offset((30, 0))
                    
            elif event.type == MOUSEBUTTONDOWN:
                
                if menu.click(event.pos): continue
                
                if event.button == 1:
                    jb1 = jb2 = None # Joint Bodies
                    jb1 = world.get_bodies_at_pos(event.pos)
                    
                    if not draw_poly:
                        draw_poly = True
                        points = []
                        points.append(event.pos)
                        
                elif event.button == 4: #scroll up
                    world.camera.inc_scale_factor(+0.02)
                    
                elif event.button == 5: # scroll down
                    world.camera.inc_scale_factor(-0.02)
            
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if jb1:
                        jb2 = world.get_bodies_at_pos(event.pos)
                        
                        if jb2:
                            if str(jb1[0]) != str(jb2[0]):
                                print "- Add Joint between:", jb1[0], jb2[0]
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
                            #world.add.rect(event.pos, width=70, height=30)
                            world.add.ball(event.pos, radius=40)

                elif event.button == 2:
                    # we want the position to become center of the screen
                    world.camera.center(event.pos)
                    
                elif event.button == 3:
                    # Add Square
                    # body = world.add.triangle(event.pos, sidelength=50)
                    # world.camera.track(body)
                    
                    bodies = world.get_bodies_at_pos(event.pos)
                    if bodies:
                        world.camera.track(bodies[0])
                            
            elif event.type == MOUSEMOTION and draw_poly:
                world.run_physics = False
                points.append(event.pos)
            
        # Clear Display
        screen.fill((255,255,255))

        # Update & Draw World
        world.update()
        world.draw()

        # Draw the Menu
        menu.draw(screen)
        
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
        clock.tick(90)
        
        # output framerate in caption
        pygame.display.set_caption("elements: %i | fps: %i" % (world.element_count, int(clock.get_fps())))

if __name__ == "__main__":
    main()
