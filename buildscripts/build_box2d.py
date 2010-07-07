#!/usr/bin/python
"""
This file is part of the 'Elements' Project
Elements is a 2D Physics API for Python (supporting Box2D2)

Copyright (C) 2008, The Elements Team, <elements@linuxuser.at>
 
Home:  http://wiki.laptop.org/go/Elements
IRC:   #elements on irc.freenode.org

Code:  http://www.assembla.com/wiki/show/elements
       svn co http://svn2.assembla.com/svn/elements                     

License:  GPLv3 | See LICENSE for the full text
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.              
"""

from os import path
from os import system

from platform import architecture
from platform import system as platformsystem
    
def force_input(question, possibilities):
	i = ""
	while i not in possibilities:
		print "%s [%s]" % (question, "/".join(possibilities)),
		i = raw_input()
	return i
	
s = platformsystem()
arch, arch2 = architecture()

print "Building Box2d & SWIG Wrapper for %s (%s)" % (s, arch)
print

if s == 'Linux': 
    import build_linux

elif s == 'Windows': 
    # Windows version doesn't follow the naming scheme, it's just as released by kne
    print "To build the sources with swig on windows, you will need to:"
    print "1. Build Box2D (see BUILDING)"
    print "2. Copy the compiled libs from Source/Gen/float/lib* to Library/"
    print "3. Download the latest swig interface to Library/ (http://svn2.assembla.com/svn/elements/box2d/Box2D.i)"
    print "4. Copy build_win.py to Library/"
    print "5. Adjust the settings in build_win.py"
    print "6. Run 'python build_win.py'"
     
#    print "Please modify the settings in buildscripts/build_win.py before building"
#    i = force_input("Proceed now?", ["y", "n"])
#    if i == "y":
#        from buildscripts import build_win

elif s == 'Darwin': 
    print "To build the sources with swig on windows, you will need to:"
    print "1. Build Box2D (see BUILDING)"
    print "2. Copy the compiled lib (Source/Gen/float/libBox2d.a to Library/"
    print "3. Download the latest swig interface to Library/ (http://svn2.assembla.com/svn/elements/box2d/Box2D.i)"
    print "4. Copy build_osx.py to Library/"
    print "5. Adjust the settings in build_win.py"
    print "6. Run 'python build_osx.py'"

#    print "Please modify the settings in buildscripts/build_osx.py before building"
#    i = force_input("Proceed now?", ["y", "n"])
#    if i == "y":
#        from buildscripts import build_osx
            
