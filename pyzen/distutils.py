from setuptools.command.test import test

class zen(test):
    """Command to run test suite under PyZen."""
    description = 'run unit tests under PyZen'

    def run(self):
        """runner"""
        print 'PyZen'