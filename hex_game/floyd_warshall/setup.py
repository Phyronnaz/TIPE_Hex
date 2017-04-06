from distutils.core import setup

import numpy
from Cython.Build import cythonize

setup(
    name='Floyd Warshall',
    ext_modules=cythonize("floyd_warshall.pyx"),
    include_dirs=[numpy.get_include()]
)
