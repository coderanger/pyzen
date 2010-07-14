from django.conf import settings
from django.core.management.base import NoArgsCommand, CommandError

from pyzen.core import main

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        main()
