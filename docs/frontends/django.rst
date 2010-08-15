Django Frontend
===============

PyZen itself can be setup as a Django application, and provides a management 
command for running the project's tests under PyZen.

Configuration
-------------

Just add ``pyzen`` to your ``INSTALLED_APPS`` setting.

Usage
-----

Run ``manage.py zen`` to start the tester process. You can give an application
label or test name using the same format as the built-in ``test`` command.

Options
~~~~~~~

``--nocolor`` : *flag, default: False*
    Disable colored output.

``-u``, ``--ui`` : *default: autodetect*
    Force the use of a specific UI module. Available options are ``win32``,
    ``osx``, ``linux``, and ``none``.
