import sys
import unittest
import types

from setuptools.command.test import test
from pkg_resources import *

from pyzen.core import main
from pyzen.runner import get_test_runner

class ZenTestProgram(unittest.TestProgram):
    
    def runTests(self):
        testRunner = self.testRunner(verbosity=self.verbosity)
        self.result = testRunner.run(self.test)

def run_tests(loader, args, path, nocolor):
    sys.path[:] = path
    loader_ep = EntryPoint.parse("x="+loader)
    loader_class = loader_ep.load(require=False)
    m = ZenTestProgram(None, None, [unittest.__file__]+args, testLoader=loader_class(), testRunner=get_test_runner(nocolor))
    return m.result

class zen(test):
    """Command to run test suite under PyZen."""
    description = 'run unit tests under PyZen'
    
    user_options = test.user_options + [
        ('ui=', 'u', 'Force the use of the given PyZen UI'),
        ('nocolor', 'c', 'Disable colored output'),
    ]
    boolean_options = ['nocolor']
    
    def initialize_options(self):
        test.initialize_options(self)
        self.ui = None
        self.nocolor = False
    
    def run_tests(self):
        main(self.ui, run_tests, self.test_loader, self.test_args, sys.path[:], self.nocolor)
