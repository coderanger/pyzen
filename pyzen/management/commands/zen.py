from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.test.simple import DjangoTestRunner
from django.test.utils import get_runner

try:
    from south.management.commands import patch_for_test_db_setup
except ImportError:
    patch_for_test_db_setup = lambda: None
    
from pyzen.core import main

class ZenTestRunner(DjangoTestRunner):
    def run(self, *args, **kwargs):
        return super(DjangoTestRunner, self).run(*args, **kwargs)

def run_tests(*test_labels, **options):
    patch_for_test_db_setup()
    verbosity = int(options.get('verbosity', 1))
    interactive = options.get('interactive', True)
    failfast = options.get('failfast', False)
    TestSuiteRunner = get_runner(settings)
    
    class NewTestSuiteRunner(TestSuiteRunner):
        def run_suite(self, suite, **kwargs):
            return ZenTestRunner(verbosity=self.verbosity, failfast=self.failfast).run(suite)
        def suite_result(self, suite, result, **kwargs):
            return result
    
    test_runner = NewTestSuiteRunner(verbosity=verbosity, interactive=interactive, failfast=failfast)
    result = test_runner.run_tests(test_labels)
    return result

class Command(BaseCommand):
    
    option_list = BaseCommand.option_list + (
        make_option('-u', '--ui', help='Force the use of the given PyZen UI'),
    )
    
    def handle(self, *test_labels, **options):
        try:
            main(options.get('ui'), run_tests, *test_labels, **options)
        except KeyboardInterrupt:
            pass
