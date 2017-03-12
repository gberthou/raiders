from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

extensions = [
    Extension("dijkstra",
        ["dijkstra.pyx"],
        extra_compile_args=["-g3"],
        extra_link_args=["-g3"]
    ),
    Extension("compiled",
        ["compiled.pyx"],
        extra_compile_args=["-g3"],
        extra_link_args=["-g3"]
    )
]

setup(ext_modules=cythonize(extensions, gdb_debug=True))
