import sys
import os.path
from setuptools import setup, find_packages, Extension
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError

# try to import numpy and Cython to build Cython extensions:
try:
    import numpy as np
    from Cython.Distutils import build_ext
    import Cython.Compiler.Options
    Cython.Compiler.Options.annotate = False
    _cython_installed = True

except ImportError:
    _cython_installed = False
    build_ext = object  # avoid a syntax error in TryBuildExt
    setup_args = {}
    print('='*80)
    print('Warning: Cython extensions will not be built as Cython is not installed!\n'\
          '         This means that the abel.direct C implementation will not be available.')
    print('='*80)



if _cython_installed:  # if Cython is installed, we will try to build direct-C

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
                print("**************************************************")
                print("WARNING: Cython extensions failed to build (used in abel.direct).\n"
                      "Typical reasons for this problem are:\n"
                      "  - a C compiler is not installed or not found\n"
                      "  - issues using mingw compiler on Windows 64bit (experimental support for now)\n"
                      "This only means that the abel.direct C implementation will not be available.\n")
                print("**************************************************")
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
            except:
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


# use README as project description on PyPI:
with open('README.md') as file:
    long_description = file.read()


setup(name='testPyAbel',  # for TestPyPI
      version='0.0.4',
      description='For testing GitHub actions',
      author='Mikhail Ryazanov',
      url='https://github.com/MikhailRyazanov/Actions',
      license='The Unlicense',
      packages=find_packages(),
      install_requires=["numpy >= 1.16",       # last for Python 2
                        "setuptools >= 44.0",  # last for Python 2
                        "scipy >= 1.2",        # oldest tested
                        "six >= 1.10.0"],
      package_data={'abel': ['tests/data/*']},
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
          # How mature is this project? Common values are
          #  3 - Alpha
          #  4 - Beta
          #  5 - Production/Stable
          'Development Status :: 3 - Alpha',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: The Unlicense (Unlicense)',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
          'Programming Language :: Python :: 3.13',
          ],
      **setup_args
      )
