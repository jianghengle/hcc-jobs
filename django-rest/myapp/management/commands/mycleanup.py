from django.core.management.base import BaseCommand
from ...models.my_session import MySession
from ...models.jupyter import Jupyter
from ...models.my_file import MyFile

class Command(BaseCommand):
    def handle(self, **options):
        MySession.clean_up()
        Jupyter.clean_up()
        MyFile.clean_up()