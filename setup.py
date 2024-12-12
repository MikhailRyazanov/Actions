import sys
import os.path
from setuptools import setup, Extension
from distutils.errors import \
    CCompilerError, DistutilsExecError, DistutilsPlatformError

# try to import NumPy and Cython to build Cython extensions:
try:
    import numpy as np
    from Cython.Distutils import build_ext
    import Cython.Compiler.Options
    Cython.Compiler.Options.annotate = False
    _build_cython = True

except ImportError:
    _build_cython = False
    build_ext = object  # avoid a syntax error in TryBuildExt
    setup_args = {}
    print('=' * 75)
    print('''\
Warning: Cython extensions will not be built, thus the abel.direct
         C implementation will not be available.
         To build them, install Cython, then reinstall PyAbel
         using pip with the --no-build-isolation option.\
         ''')
    print('=' * 75)

if _build_cython:  # declarations for building direct-C Cython extension

    if sys.platform == 'win32':
        extra_compile_args = ['/Ox', '/fp:fast']
        libraries = []
    else:
        extra_compile_args = ['-Ofast', '-g0']
        libraries = ["m"]

    # Optional compilation of Cython modules adapted from
    # https://github.com/bsmurphy/PyKrige which was itself
    # adapted from a StackOverflow post

    ext_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError)

    class TryBuildExt(build_ext):
        """Class to  build the direct-C extensions."""

        def build_extensions(self):
            """Try to build the direct-C extension."""
            try:
                build_ext.build_extensions(self)
            except ext_errors:
                print('*' * 75)
                print('''\
WARNING: Cython extensions failed to build (used in abel.direct). This only
         means that the abel.direct C implementation will no be available.
         Typical reasons for this problem are:
         - a C compiler is not installed or not found,
         - issues using mingw compiler on Windows 64bit (experimental).\
                      ''')
                print('*' * 75)
                if os.environ.get('CI'):
                    # running on Travis CI or Appveyor CI
                    if sys.platform == 'win32' and sys.version_info < (3, 0):
                        # Cython extensions are not built on Appveyor (Win)
                        # for PY2.7. See PR #185
                        pass
                    else:
                        raise
                else:
                    # regular install, Cython extensions won't be compiled
                    pass
            except Exception as e:
                print('*' * 75)
                print('ERROR in building Cython extensions:')
                print(e)
                print('*' * 75)
                raise

    ext_modules = [
        Extension("abel.lib.direct",
                  [os.path.join("abel", "lib", "direct.pyx")],
                  include_dirs=[np.get_include()],
                  libraries=libraries,
                  extra_compile_args=extra_compile_args)]

    setup_args = {'cmdclass': {'build_ext': TryBuildExt},
                  'include_dirs': [np.get_include()],
                  'ext_modules': ext_modules}

import datetime
long_description = 'Long description generated in setup.py at ' + \
                    str(datetime.datetime.now()) + '.'

setup(long_description=long_description, **setup_args)
