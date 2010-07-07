Box2D Python Bindings 

INSTALL
-------

Files go in Box2D\Source.

 1. patch -p0 < Makefile.patch
  2.a. make pythonlib && setup.py install
   [ Other targets: python_install, python_egg, python_installer_win32 ]
    b. make python_install

The patch for now just includes the Makefile.python, so it's just for convenience.
You could very well just do 'make && make -f Makefile.python python_install'


kne - 4/18/2008