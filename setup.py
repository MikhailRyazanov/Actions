from setuptools import setup, find_packages

setup(name='Actions',
      version='0.0.1',
      description='For testing GitHub actions',
      author='Mikhail Ryazanov',
      url='https://github.com/MikhailRyazanov/Actionsl',
      license='The Unlicense',
      packages=find_packages(),
      install_requires=["numpy >= 1.16",       # last for Python 2
                        "setuptools >= 44.0",  # last for Python 2
                        "scipy >= 1.2",        # oldest tested
                        "six >= 1.10.0"],
      package_data={'abel': ['tests/data/*']},
      classifiers=[
          # How mature is this project? Common values are
          #  3 - Alpha
          #  4 - Beta
          #  5 - Production/Stable
          'Development Status :: 3 - Alpha',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: Unlicense',

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
      )
