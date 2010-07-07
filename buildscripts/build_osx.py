#!/usr/bin/python
import os, sys, re
#------------------------------------------------
#notes:
# put this in Box2D/Library/
#
# be sure to modify all of the paths in this section
# requires swig 1.3.34, python 2.5. 
# DO NOT use fink! use the regular installer.

import distutils.sysconfig
python_dir  = "/sw/lib/python2.5/"
wrapper_opts="-c -I" + distutils.sysconfig.get_python_inc() + " -L" + distutils.sysconfig.get_python_lib()
collect2_path="/usr/libexec/gcc/i686-apple-darwin9/4.0.1/collect2"
collect2_opts="*.o /usr/lib/gcc/i686-apple-darwin9/4.0.1/crt3.o -arch i386 -weak_reference_mismatches non-weak -o _Box2D2.so -L" + distutils.sysconfig.get_python_lib() + " -L/usr/lib/gcc/i686-apple-darwin9/4.0.1/ -flat_namespace -undefined suppress -bundle -lstdc++ -lgcc_s.10.4 -lgcc -lSystem"

# change wrapper_opts to reflect your python version (if not 2.5!)
#---------------

gpp_opts    ="-c -O3" #-g for debug
swig_opts   ="-python -c++ -includeall -ignoremissing"
iface_templ ="Box2D.i"
#------------------------------------------------

ar_path   = "ar"
gpp_path  ="g++"
swig_path ="swig"

gpp_opts =gpp_opts.replace("%pythondir%", python_dir)
swig_opts =swig_opts.replace("%pythondir%", python_dir)
wrapper_opts=wrapper_opts.replace("%pythondir%", python_dir)

sourcefiles = []
allsubdirs   = []
flist  = os.walk("../Source/")
for (base, subdirs, files) in flist:
    for subdir in subdirs:
        if subdir[0]=='.': continue
        if subdir.find('.svn'): continue
        allsubdirs.append( os.path.join(base, subdir) )

    for file in files:
#	print file
        if file[-4:].lower()==".cpp":
            sourcefiles.append(os.path.join(base, file))

#-- compile src
print "Rebuild source? [Y/n]"
rebuild = sys.stdin.read(1)
if rebuild.lower() == "y" or rebuild.strip()=="":
    for file in sourcefiles:
        line=" ".join([gpp_path, gpp_opts, file])
        print "->", line
        if os.system(line) != 0:
            raise Exception, "Build error (g++)"
            exit()

flist  = os.listdir(".")
o_files=[]
for file in flist:
    if os.path.normcase(file[-2:])==".o":
        o_files.append(os.path.join(".", file))

#-- ar

ar_cmd=ar_path + " rcvs libBox2D.a " + " ".join(o_files)
print "------------------------------------------------------------------------------"
print "Building static library: -> ", ar_cmd

if os.system(ar_cmd) != 0:
    raise Exception, "Build error (ar)"
    exit()

#-- swig

run=" ".join([swig_path, swig_opts, "-I" + " -I".join(allsubdirs) , iface_templ])
print "------------------------------------------------------------------------------"
print "Executing swig ->", run
if os.system(run) != 0:
    raise Exception, "Build error (swig with template interface)"

#-- build wrapper -> .so
run=" ".join([gpp_path, os.path.splitext(iface_templ)[0] + "_wrap.cxx", wrapper_opts])
print "------------------------------------------------------------------------------"
print "Building .so ->", run
if os.system(run) != 0:
    raise Exception, "Build error (swig DLL wrapper compilation)"

#-- link into a python liby
run=" ".join([collect2_path, collect2_opts])
print "------------------------------------------------------------------------------"
print "Linking to a python lib ->", run
if os.system(run) != 0:
    raise Exception, "Build error (swig DLL wrapper compilation)"

#cmd="sudo cp _Box2D2.so /sw/lib/python2.5/Box2D2.pyo"
#print "->", cmd
#os.system(cmd)
#cmd="sudo cp Box2D2.py /sw/lib/python2.5/Box2D2.py"
#print "->", cmd
#os.system(cmd) 


