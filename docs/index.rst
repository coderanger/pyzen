PyZen
=====

PyZen is a continuous test runner for paranoid developers. As long as the
script is running, it will monitor for changes in your code and re-run your
test suite when needed. There are frontends for multiple frameworks as well
as several notification UIs.

Features
--------

* Monitor source code and run tests on change
* OS-specific async notification UI
* Colored test output

Installation
------------

PyZen can be installed from PyPI using easy_install::
    
    $ easy_install PyZen
    
or pip::
    
    $ pip install PyZen
    

Frontends
---------

PyZen provides multiple frontends to collect tests and run the continuous
tester.

Django
~~~~~~

To setup PyZen under Django add ``pyzen`` to your ``INSTALLED_APPS`` setting.
The run ``manage.py zen`` to start the tester process. You can give an
application label or test name using the same format as the built-in ``test``
command.

Flask
~~~~~

The Flask frontend is maintained as separate package, `Flask-Zen`_.

.. _Flask-Zen: http://pypi.python.org/pypi/Flask-Zen

Distutils
~~~~~~~~~

The PyZen package provides a distutils command ``zen`` that will run the test
suite configured in setup.py under PyZen. Run ``setup.py zen`` to start the
tester process.

Standalone
~~~~~~~~~~

The ``pyzen`` script provides a wrapper to run any test script under PyZen.
Run ``pyzen yourscript.py arg1 arg2 ...`` to start the tester process. No
configuration options are available at this time.

Options
~~~~~~~

``--nocolor`` : *flag, default: False*
    Disable colored output.

``-u``, ``--ui`` : *default: autodetect*
    Force the use of a specific UI module. Available options are ``win32``,
    ``osx``, ``linux``, and ``none``.

UIs
---

PyZen provides a UI to indicate the current test status after each run, even
if the console is in the background. In addition to the three
platform-specific interfaces, the ``none`` interface will disable this
display. See the frontend documentation for details, but most frontends offer
a ``--ui`` option to override the autodetection.

Win32
~~~~~

The default UI on Windows is a systray icon indicating the current test status
and balloon notifications after each run. This UI is tested on Windows XP and
higher, though it may work with Windows 2000.

OS X
~~~~

The default UI on OS X uses Growl via AppleScript. A Growl notification is
posted after each test run.

Linux
~~~~~

The default UI on Linux uses libnotify via the pynotify library. This is
installed by default on current versions of Ubuntu. If pynotify is not found,
the interface will be disabled.

Test Runner
-----------

By default PyZen enhances the test output with color. It is known to work on
both Windows and \*nix systems. Most frontends have a ``--nocolor`` option to
disable it if needed.