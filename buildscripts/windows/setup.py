#!/usr/bin/env python

"""
Test
"""

from distutils.core import setup, Extension
import os

if os.getenv("TARGET_FLOAT32_IS_FIXED"):
    # I can't find a purpose for this yet, but maybe there is...
    package_dir = 'Gen\\python-fixed'
    package_type="fixed"
else:
    package_dir = 'Gen\\python-float'
    package_type="float"

init = open(os.path.join(package_dir, "__init__.py"), "w")
init.write("from Box2D2 import *")
init.close()

box2d_version = "2.0.1"
release_number = 2
version_str = box2d_version + 'b' + str(release_number)

setup (name = 'Box2D',
        version = version_str,
        packages=["Box2D2"],
        package_dir = {'Box2D2': package_dir},
        package_data={"Box2D2" : ["_Box2D2.pyd"] },

        author      = "kne",
        author_email = "sirkne at gmail dot com",
        description = "Box2D Python Wrapper (%s build)" % package_type,
        license="zlib",
        url="http://pybox2d.googlepages.com",
        long_description = """Wraps Box2D (currently version %s) for usage in Python.
        For more information, see the homepage or Box2D's homepage at http://www.box2d.org .
        Wiki: http://www.box2d.org/wiki/index.php?title=Box2D_with_Python
        Ports forum: http://www.box2d.org/forum/viewforum.php?f=5
        """ % (box2d_version),
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: zlib/libpng License',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python',
            'Games :: Physics Libraries'
        ]
        )

