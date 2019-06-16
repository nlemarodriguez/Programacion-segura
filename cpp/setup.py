from distutils.core import setup, Extension
from Cython.Build import cythonize

ext = Extension("pylibfromcpp",
              sources=["pylibfromcpp.pyx", "milibreria.cpp"],
              language="c++",)

setup(name = "cython_pylibfromcpp", ext_modules = cythonize(ext))
