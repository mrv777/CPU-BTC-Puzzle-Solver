from setuptools import setup, Extension
from Cython.Build import cythonize
import os
import numpy as np

# M1 Mac-specific optimizations
extra_compile_args = [
    '-O3',
    '-march=native',
    '-mtune=native',
    '-ffast-math',
]

if os.uname().machine == 'arm64':  # M1/M2 Mac
    extra_compile_args.extend([
        '-mcpu=apple-m1',
        '-mtune=native'
    ])

extensions = [
    Extension(
        "bitcoin_utils",
        ["bitcoin_utils.pyx"],
        extra_compile_args=extra_compile_args,
        extra_link_args=['-framework', 'Security'] if os.uname().machine == 'arm64' else [],
        include_dirs=[np.get_include(), '/opt/homebrew/opt/openssl@3/include'],
        library_dirs=['/opt/homebrew/opt/openssl@3/lib'],
        libraries=['crypto']
    )
]

setup(
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            'language_level': "3",
            'boundscheck': False,
            'wraparound': False,
            'initializedcheck': False,
            'cdivision': True,
        }
    )
)
