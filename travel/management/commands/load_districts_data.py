import requests
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load districts data into db"

    def handle(self, *args, **kwargs): ...
