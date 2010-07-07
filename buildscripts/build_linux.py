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
from os import chdir
from os import popen
from os import popen4

from sys import argv
from sys import exit

from urllib2 import urlopen

def get_latest_swig_interface_file():
    return urlopen("http://svn2.assembla.com/svn/elements/Box2D.i").read().strip()

def cmd_output(cmd):
        (pi, po) = popen4(cmd)
        return po.read().strip()
        
class compiler_linux:
    def check_system(self):
        # returns true if all requirements are found, false if not
        # need: c++ (==) g++, swig, python2.4-dev or python2.5-dev
        ok = True
        print "Checking system for requirements..."
        
        print "- Check for python ...",
        s = cmd_output("python --version")
        print s
        if "python 2.5" in s.lower():
            python_ver="2.5"
        elif "python 2.5" in s.lower():
            python_ver="2.4"
        else:
            python_ver="2.x"
        self.python_ver = python_ver
        
        print "- Check for svn ......",
        s = popen("which svn").read().strip()
        if len(s) > 0:
            (pi, po) = popen4("svn --version")
            s = po.read()
            s2 = s.split("\n")
            for x in s2:
                if "version" in x:
                    print x
                    break
        else: 
            ok = False
            print "not found - please install 'subversion'"
            
        print "- Check for g++ ......",
        s = popen("which g++").read().strip()
        if len(s) > 0:
            s = popen("g++ --version").read().strip()
            s = s.split("\n")
            for x in s:
                if "g++" in x:
                    print x
                    break
        else: 
            ok = False
            print "not found - please install 'g++'"
        
        print "- Check for swig .....",
        s = popen("which swig").read().strip()
        if len(s) > 0:
            s = popen("swig -version").read().strip()
            s = s.split("\n")
            for x in s:
                if "Version" in x:
                    print x
                    break
        else: 
            ok = False
            print "not found - please install 'swig'"
            
        print "- Check for python%s-dev ..." % python_ver,
        s = popen("locate Python.h").read().strip()
        if "/usr/include/python%s" % python_ver in s:
            print "ok"
        else:  
            print "not found - please install python%s-dev" % python_ver
            ok = False
            
        return ok
        
    def patch_makefile(self, makefile_text):
        if "TARGETS+= Gen/float/libbox2d.so" in makefile_text:
            print "already patched"
            return False

        m_arr = makefile_text.split("\n")
        i = 0        
        for m in m_arr:
           mx = m.replace(" ", "").replace("\t", "").lower()
#           print mx
           if "targets=gen/float/libbox2d.a" in mx:
               m_arr.insert(i+1, "TARGETS+= Gen/float/libbox2d.so")
           
           elif "cxxflags=" in mx:
               print ">>", m
               print mx
               print "> %s asd" % str(m)
               m_arr[i] = "CXXFLAGS=	-g -O2 -fPIC"
               
           elif "gen/float/libbox2d.a:$(" in mx:
               m_arr.insert(i+4, "Gen/float/libbox2d.so:  $(addprefix Gen/float/,$(SOURCES:.cpp=.o))\n\t$(CXX) -shared -fPIC -C $^ -o $@ -lm -lgcc\n")
               
           i += 1
        return "\n".join(m_arr)
        
    def make(self):
        chdir ("Source")

        f = open("Makefile")
        makefile = f.read().strip()
        f.close()
        
        makefile_new = self.patch_makefile(makefile)
        if makefile_new != False:
            f = open("Makefile", "w")
            f.write(makefile_new.strip())
            f.close()

        # Make
        system("make clean")
        system("make")
        
        # Copy and leave
        system("cp -v Gen/float/libbox2d.* ../Library/")
        chdir("..")
        
        print "Compiling finished"
        
    def make_swig(self):
        chdir("Library")
        swig_i = get_latest_swig_interface_file()
        
        f = open("Box2D.i", "w")
        f.write(swig_i)
        f.close()
        
        print "Creating Swig Wrapper..."
        system("swig -python -c++ -includeall -ignoremissing Box2D.i")
        
        print "Compiling Swig Wrapper..."
        system("g++ -shared -fPIC -o _Box2D2.so -O3 -I/usr/include/python2.5 -L/usr/lib/python2.5 Box2D_wrap.cxx libbox2d.a")

        print "Stripping Library"
        system("strip _Box2D2.so")
        
        chdir("..")

def quit(status=0):
    print
    exit(status)
    
def force_input(question, possibilities):
	i = ""
	while i not in possibilities:
		print "%s [%s]" % (question, "/".join(possibilities)),
		i = raw_input()
	return i


compiler = compiler_linux()
sysok = compiler.check_system()
print

if not sysok:
    i = force_input("Try to compile anyway?", ["y", "n"])
    if i == "n":
        quit()
    
pathname = path.dirname(argv[0]) 
abspath = path.abspath(pathname)
#abspath = "/tmp"


print "Use [%s] (work in box2d/)?" % abspath,
i = force_input("", ["y", "n"])

if i == "y":
    workpath = abspath
else:
    workpath = ""
    while not path.isdir(workpath):
        print "Please enter path:",
        workpath = raw_input()

# Start Doing Things
print
workpath = path.abspath(workpath)
chdir(workpath)

print "Changed to %s" % workpath
print "Starting SVN Checkout of Box2D (r135)"

# Check out SVN
system("svn co https://box2d.svn.sourceforge.net/svnroot/box2d/Source box2d/Source -r 135")

# Apply Makefile Patch to Source/Makefile
chdir("box2d")

system("mkdir Library")

# This will compile the floating point Box2d library and copy it to box2d/Library
compiler.make()

# This will download and compile the Swig Interface
# Script is now in the box2d/ directory
compiler.make_swig()

print
print "All done. If there were no error messages, you can find the library files here now:"
print "  - %s/box2d/swig/Box2D2.py" % workpath
print "  - %s/box2d/swig/_Box2D2.so" % workpath
