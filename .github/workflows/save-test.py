"""
cibuildwheel doesn't provide any reasonable variables for naming pytest results
file, neither any tools to supply these files with the built wheels, so all
this work is done by this script.

It must be called after running pytest, in the same directory, with the
{package} and {wheel} cibuildwheel placeholders as its arguments.
"""
import os
import platform
import sys
import shutil

package = sys.argv[1]  # full path to package directory
wheel = os.path.basename(sys.argv[2])  # wheel file name

if platform.system() == 'Linux':
    out = f'/output/{wheel}.xml'  # in container
else:
    out = f'{package}/wheels/{wheel}.xml'  # assuming "--output-dir wheels"

print('Saving results to', out)
os.makedirs(os.path.dirname(out), exist_ok=True)  # (might not exist yet)
shutil.move('pytest.xml', out)
