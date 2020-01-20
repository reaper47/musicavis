from subprocess import call

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Start a celery server'

    def handle(self, *args, **options):
        call(['celery', '-A', 'musicavis', 'worker', '-l', 'info'])
