#!/usr/bin/env python

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup

LONG_DESCRIPTION = \
"""
Elements is a 2D Physics API for Python

Copyright (C) 2008-9 The Elements Team <elements@linuxuser.at>

Home:  http://elements.linuxuser.at
IRC:   #elements on irc.freenode.org

Code:  http://www.assembla.com/wiki/show/elements
       svn co http://svn2.assembla.com/svn/elements                     

License:  GPLv3 | See LICENSE for the full text
"""

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: POSIX",
    "Topic :: Games/Entertainment",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Programming Language :: Python",
    ]


setup(
    name            ='Elements',
    version         ='0.13',
    description     ='Elements -- Simplified 2D Physics',
    author          ='Elements Team',
    author_email    ='elements@linuxuser.at',
    url             ='http://www.assembla.com/spaces/elements/',
    long_description=LONG_DESCRIPTION,
    classifiers     =CLASSIFIERS,
    packages        =['elements'],
    install_requires=['Box2D >= 2.0.2b1'],
     )

