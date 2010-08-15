Distutils Frontend
==================

The PyZen package provides a distutils command ``zen`` that will run the
test suite configured in setup.py under PyZen.

Usage
-----

Run ``setup.py zen`` to start the tester process.

Options
~~~~~~~

``--nocolor`` : *flag, default: False*
    Disable colored output.

``-u``, ``--ui`` : *default: autodetect*
    Force the use of a specific UI module. Available options are ``win32``,
    ``osx``, ``linux``, and ``none``.
