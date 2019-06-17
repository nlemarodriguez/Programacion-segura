from distutils.core import setup, Extension
from Cython.Build import cythonize

ext = Extension("pylibfromcpp", sources=["pylibfromcpp.pyx", "Filter_Black_White.c"], language="c",)

extensions = [
    Extension("pylibfromcpp", sources=["pylibfromcpp.pyx", "Filter_Black_White.c"], language="c",),
    Extension("pylibfromcpp_mono_color", sources=["pylibfromcpp_mono_color.pyx", "Filter_Mono_Color.c"], language="c",),
]

setup(name = "cython_pylibfromcpp", ext_modules = cythonize(extensions))
