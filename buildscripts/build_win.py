#!/usr/bin/python
import os, sys, re
#------------------------------------------------
#notes: 
# - requires a recent version of swig (preferrably 1.3.35)
# - python 2.5 only has been tested
# - update the paths appropriately 
# - if you still get -lpython25 errors, try downloading libpython25.a and statically linking it (i.e., replace -lpython25 with libpython25.a in wrapper_opts)
#user settings, kinda
mingw_path  ="c:\\mingw\\"
swig_dir    ="c:\\python25\\swig\\"
python_dir  ="c:\\python25\\"
gpp_opts    ="-c -O3" #-g for debug
swig_opts   ="-python -w -c++ -O -w201 -includeall -ignoremissing"
wrapper_opts="-shared -O3 -o _Box2D2.pyd -I%pythondir%include -L%pythondir%libs libBox2D.a -lpython25"
iface_templ ="Box2D.i"
# change wrapper_opts to reflect your python version
# if it can't locate your python library, try downloading libpython25.a and statically linking it
#------------------------------------------------

mingw_bin =os.path.join(mingw_path, "bin\\")
ar_path   =os.path.join(mingw_bin, "ar.exe")
gpp_path  =os.path.join(mingw_bin, "g++.exe")
swig_path =os.path.join( swig_dir, "swig.exe")

gpp_opts =gpp_opts.replace("%pythondir%", python_dir)
swig_opts =swig_opts.replace("%pythondir%", python_dir)
wrapper_opts=wrapper_opts.replace("%pythondir%", python_dir)

sourcefiles, includefiles = [], []
flist  = os.walk("..\\Source\\")
for (base, subdirs, files) in flist:
    for file in files:
        if os.path.normcase(file)[-2:]==".h":
            includefiles.append(os.path.join(base, file))
        if os.path.normcase(file)[-4:]==".cpp":
            sourcefiles.append(os.path.join(base, file))

#-- compile src
print "Rebuild source? [Y/n]"
rebuild = sys.stdin.read(1)
#rebuild = "n"
if rebuild.lower() == "y" or rebuild.strip()=="":
    for file in sourcefiles:
        line=" ".join([gpp_path, gpp_opts, file])
        print "->", line
        if os.system(line) != 0:
            os.system("pause")
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
    os.system("pause")
    raise Exception, "Build error (ar)"

#-- swig

run=" ".join([swig_path, swig_opts, iface_templ])
print "------------------------------------------------------------------------------"
print "Executing swig ->", run
if os.system(run) != 0:
    os.system("pause")
    raise Exception, "Build error (swig with template interface)"

#-- build DLL wrapper
run=" ".join([gpp_path, os.path.splitext(iface_templ)[0] + "_wrap.cxx", wrapper_opts])
print "------------------------------------------------------------------------------"
print "Building DLL ->", run
if os.system(run) != 0:
    os.system("pause")
    raise Exception, "Build error (swig DLL wrapper compilation)"


def do_copy(src, dest):
    print "Copying %s to %s..." % (src, dest)
    os.system(" ".join(["copy", src, dest]))

do_copy("_Box2D2.pyd", os.path.join(python_dir, "dlls\\_Box2D2.pyd"))
do_copy("Box2D2.py", os.path.join(python_dir, "lib\\Box2D2.py"))

#elements_dir = "C:\\dev\\elements\\elements\\elements\\box2d\\box2d_win"
#do_copy("_Box2D2.pyd", os.path.join(elements_dir, "_Box2D2.pyd"))
#do_copy("Box2D2.py", os.path.join(elements_dir, "Box2D2.py"))

os.system("pause")

