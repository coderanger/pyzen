from setuptools import Command

class zen(Command):
    """setuptools Command"""
    description = "run my command"
    user_options = []
    def initialize_options(self):
        """init options"""
        pass

    def finalize_options(self):
        """finalize options"""
        pass

    def run(self):
        """runner"""
        print 'PyZen'