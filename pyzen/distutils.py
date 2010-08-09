from setuptools.command.test import test
from pkg_resources import *

class zen(test):
    """Command to run test suite under PyZen."""
    description = 'run unit tests under PyZen'

    def run_tests(self):
        import unittest
        loader_ep = EntryPoint.parse("x="+self.test_loader)
        loader_class = loader_ep.load(require=False)
        unittest.main(
            None, None, [unittest.__file__]+self.test_args,
            testLoader = loader_class()
        )
