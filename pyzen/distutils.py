import sys
import unittest
import types

from setuptools.command.test import test
from pkg_resources import *

from pyzen.core import main

class ZenTestProgram(unittest.TestProgram):
    
    def runTests(self):
        if self.testRunner is None:
            self.testRunner = TextTestRunner

        if isinstance(self.testRunner, (type, types.ClassType)):
            try:
                testRunner = self.testRunner(verbosity=self.verbosity)
            except TypeError:
                # didn't accept the verbosity argument
                testRunner = self.testRunner()
        else:
            # it is assumed to be a TestRunner instance
            testRunner = self.testRunner
        self.result = testRunner.run(self.test)

def run_tests(loader, args, path):
    sys.path[:] = path
    loader_ep = EntryPoint.parse("x="+loader)
    loader_class = loader_ep.load(require=False)
    m = ZenTestProgram(None, None, [unittest.__file__]+args, testLoader=loader_class())
    return m.result

class zen(test):
    """Command to run test suite under PyZen."""
    description = 'run unit tests under PyZen'

    def run_tests(self):
        main(None, run_tests, self.test_loader, self.test_args, sys.path[:])
