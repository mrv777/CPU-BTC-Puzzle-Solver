from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("bitcoin_utils.pyx"),
    zip_safe=False,
)
