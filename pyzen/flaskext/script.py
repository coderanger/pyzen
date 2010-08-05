import sys
import unittest
import inspect
import os.path
import fnmatch

from flaskext.script import Command, Option

from pyzen.core import main

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

def run_tests(app, pattern, start_dir, verbosity):
    print start_dir
    loader = ZenTestLoader()
    suite = loader.discover(start_dir, pattern, start_dir)
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    return len(result.failures)

class Test(Command):
    """Run app tests."""
    
    def __init__(self, pattern='*/tests/*.py;*/tests.py', start_dir=None, verbosity=0):
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
        ]
    
    def run(self, app, pattern, start_dir, verbosity):
        failures = run_tests(app, pattern, start_dir, verbosity)
        if failures:
            sys.exit(1)


class ZenTest(Test):
    """Run app tests continuously."""
    
    def run(self, app, pattern, start_dir, verbosity):
        try:
            main(run_tests, app, pattern, start_dir, verbosity)
        except KeyboardInterrupt:
            pass