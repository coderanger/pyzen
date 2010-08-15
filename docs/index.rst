PyZen
=====

PyZen is a continuous test runner for paranoid developers. As long as the
script is running, it will monitor for changes in your code and re-run your
test suite when needed. There are frontends for multiple frameworks as well
as several notification UIs.

Installation
------------

PyZen can be installed from PyPI using easy_install::
    
    $ easy_install PyZen
    
or pip::
    
    $ pip install PyZen
    

Frontends
---------

To use PyZen you need a frontend for your environment. The Django, Flask, and
distutils frontends provide hooks into their respective frameworks, while the
standalone frontend provides a wrapper environment to run an arbitrary script
in.

.. toctree::
    :maxdepth: 1
    
    frontends/django
    frontends/flask
    frontends/distutils
    frontends/standalone

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