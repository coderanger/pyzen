import sys
import unittest
import inspect
import os.path
import fnmatch

from flaskext.script import Command, Option

from pyzen.core import main
from pyzen.runner import ColoredTextTestRunner

try:
    from unittest2 import TestLoader
except ImportError:
    try:
        from discover import DiscoveringTestLoader as TestLoader
    except ImportError:
        from pyzen.discover import DiscoveringTestLoader as TestLoader

__all__ = ['Test', 'ZenTest']

class ZenTestLoader(TestLoader):
    
    def _match_path(self, path, full_path, pattern):
        for pat in pattern.split(';'):
            if fnmatch.fnmatch(full_path, pat):
                return True
        return False

def run_tests(app, pattern, start_dir, verbosity, nocolor):
    print start_dir
    loader = ZenTestLoader()
    suite = loader.discover(start_dir, pattern, start_dir)
    if nocolor:
        runner = unittest.TextTestRunner
    else:
        runner = ColoredTextTestRunner
    result = runner(verbosity=verbosity).run(suite)
    return result

class Test(Command):
    """Run app tests."""
    
    def __init__(self, pattern='*/tests/*.py;*/tests.py', start_dir=None, verbosity=1):
        if start_dir is None:
            # Find the file that called this constructor and use its directory
            for f in inspect.stack():
                start_dir = os.path.dirname(os.path.abspath(f[1]))
                if start_dir != os.path.dirname(__file__):
                    break
            else:
                raise ValueError('Unable to find start_dir')
        self.default_pattern = pattern
        self.default_start_dir = start_dir
        self.default_verbosity = verbosity
    
    def get_options(self):
        return [
            Option('-p', '--pattern', dest='pattern', default=self.default_pattern),
            Option('-s', '--start_dir', dest='start_dir', default=self.default_start_dir),
            Option('-v', '--verbosity', dest='verbosity', default=self.default_verbosity),
            Option('--nocolor', action='store_true', default=False, help='Disable colored output'),
        ]
    
    def run(self, app, pattern, start_dir, verbosity, nocolor):
        result = run_tests(app, pattern, start_dir, verbosity, nocolor)
        if result.failures or result.errors:
            sys.exit(1)


class ZenTest(Test):
    """Run app tests continuously."""
    
    def get_options(self):
        options = super(ZenTest, self).get_options()
        options.append(Option('-u', '--ui', help='Force the use of the given PyZen UI'))
        return options
    
    def run(self, app, pattern, start_dir, verbosity, ui, nocolor):
        try:
            main(ui, run_tests, app, pattern, start_dir, verbosity, nocolor)
        except KeyboardInterrupt:
            pass