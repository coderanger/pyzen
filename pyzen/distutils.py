import sys
import unittest

from setuptools.command.test import test
from pkg_resources import *

from pyzen.core import main

def run_tests(loader, args, path):
    sys.path[:] = path
    loader_ep = EntryPoint.parse("x="+loader)
    loader_class = loader_ep.load(require=False)
    fail = False
    try:
        unittest.main(None, None, [unittest.__file__]+args, testLoader=loader_class())
    except SystemExit, e:
        if e.code:
            fail = True
    
    result = unittest.TestResult()
    result.total = -1
    # len(failures)==1 indicates failure
    if fail:
        result.failures.append(None)
    return result

class zen(test):
    """Command to run test suite under PyZen."""
    description = 'run unit tests under PyZen'

    def run_tests(self):
        main(None, run_tests, self.test_loader, self.test_args, sys.path[:])
