import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """DJANGO COMMAND TO PAUSE EXECUTION UNTIL DATABASE IS AVAILABLE"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for Database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, Waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Databse available'))
