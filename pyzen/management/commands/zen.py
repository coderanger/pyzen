from django.conf import settings
from django.core.management.base import NoArgsCommand, CommandError
from django.test.simple import DjangoTestRunner
from django.test.utils import get_runner

try:
    from south.management.commands import patch_for_test_db_setup
except ImportError:
    patch_for_test_db_setup = lambda: None
    
from pyzen import reload

class ZenTestRunner(DjangoTestRunner):
    
    def run(self, *args, **kwargs):
        return super(DjangoTestRunner, self).run(*args, **kwargs)

def run_tests(**options):
    patch_for_test_db_setup()
    verbosity = int(options.get('verbosity', 1))
    interactive = options.get('interactive', True)
    failfast = options.get('failfast', False)
    TestSuiteRunner = get_runner(settings)
    
    class NewTestSuiteRunner(TestSuiteRunner):
        def run_suite(self, suite, **kwargs):
            return ZenTestRunner(verbosity=self.verbosity, failfast=self.failfast).run(suite)
    
    test_runner = NewTestSuiteRunner(verbosity=verbosity, interactive=interactive, failfast=failfast)
    failures = test_runner.run_tests([])

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        reload.main(run_tests, None)
