#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform
import os

import numpy as np


class Transform(object):
    def __init__(self, IM, direction='inverse'):
        self.IM = IM
        self.direction = direction

        self.transform = direction.upper()


# Default directory for cached basis sets;
# used by set_basis_dir() and get_basis_dir().
# DON'T access this variable directly!
_basis_dir = ''


def set_basis_dir(basis_dir='', make=True):
    """
    Changes the path to the directory for saving/loading cached basis sets that
    transform methods use by default.

    Parameters
    ----------
    basis_dir : str or None
        absolute or relative path. Passing ``''`` (default) resets to the
        system-dependent default path, see :func:`default_basis_dir`. For the
        current working directory (as in PyAbel up to v0.8.4), use ``'.'``. To
        disable basis-set caching on disk, use ``None``.
    make : bool
        create the directory if it does not exist (default: yes)

    Returns
    -------
    None
    """
    global _basis_dir

    if basis_dir == '':
        _basis_dir = default_basis_dir()
    else:
        _basis_dir = basis_dir

    if make:
        _make_basis_dir()  # (safe for None)


def get_basis_dir(make=False):
    """
    Gets the path to the directory for saving/loading cached basis sets that
    transform methods use by default. If not changed by :func:`set_basis_dir`,
    it depends on the operating system, see :func:`default_basis_dir`.

    Parameters
    ----------
    make : bool
        create the directory if it does not exist (default: no)

    Returns
    -------
    path : str or None
        absolute or relative path if disk caching is enabled,
        otherwise ``None``
    """
    global _basis_dir

    if _basis_dir == '':
        set_basis_dir('', make)

    return _basis_dir


def _make_basis_dir():
    """
    Internal utility function.

    Makes sure that the default basis-set directory (if enabled) exists.
    """
    if _basis_dir is None or os.path.exists(_basis_dir):
        return

    try:
        os.makedirs(_basis_dir)
    except Exception as e:
        print('Cannot create the directory\n"{}"\n'
              'for saving/loading basis sets:'.format(_basis_dir))
        raise


def default_basis_dir():
    r"""
    Gets full path to the system-dependent default directory for saving/loading
    cached basis sets:

    Linux (and other Unix-like):
        ``~/.cache/PyAbel`` (or ``$XDG_CACHE_HOME/PyAbel`` if set)
    macOS:
        ``/Users/<user>/Library/Caches/PyAbel``
    Windows:
        ``<user profile>\AppData\Local\PyAbel\cache`` (or
        ``%LOCALAPPDATA%\PyAbel\cache`` if set). See important notes below.

    Parameters
    ----------
    None

    Returns
    -------
    path : str
        full path to the system-dependent default basis-sets directory


    .. admonition:: Notes for MS Windows users

      * Python installed from Microsoft Store redirects subdirectory creation
        in ``AppData\Local`` to a `"private per-user, per-app location"
        <https://learn.microsoft.com/en-us/windows/msix/desktop/desktop-to-uwp-behind-the-scenes>`__
        ``AppData\Local\Packages\Python...\LocalCache\Local`` (see `Using
        Python on Windows / Known Issues
        <https://docs.python.org/3/using/windows.html#known-issues>`__).
        However, if ``AppData\Local\PyAbel\`` already exists (for example, was
        manually created *not* from Python), apparently it should be usable.

      * Old Windows versions (2000, XP, Server 2003) by default don't set the
        ``LOCALAPPDATA`` environment variable, so PyAbel will create and use
        the ``AppData\Local`` subtree in the user profile folder. This is
        probably fine, but not how it should be. To use the standard location,
        please do ::

            set LOCALAPPDATA=%USERPROFILE%\Local Settings\Application Data

        before starting Python. Or permanently set it in “Environment
        Variables” from Windows “System Properties”.
    """
    # Based on the appdirs module, https://github.com/ActiveState/appdirs
    # (see https://github.com/ActiveState/appdirs/blob/master/appdirs.py)
    system = platform.system()

    if system == 'Darwin':  # macOS
        return os.path.expanduser('~/Library/Caches/PyAbel')

    if system == 'Windows':
        return os.path.join(os.getenv('LOCALAPPDATA',
                                      os.path.expanduser(r'~\AppData\Local')),
                            r'PyAbel\cache')

    # Linux and other
    return os.path.join(os.getenv('XDG_CACHE_HOME',
                                  os.path.expanduser('~/.cache')),
                        'PyAbel')

    # system == 'Java' is ignored as useless -- Jython does not support NumPy
