from django.core.management.base import BaseCommand, CommandError
from guidebook.models import *
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args):
        for river in River.objects.all():
            Place.objects.create(river=river, created_by_user=User.objects.all().first(), location=river.get_in, description=f'{river.river_name}, main put in', place_type="put")
            Place.objects.create(river=river, created_by_user=User.objects.all().first(), location=river.get_out, description=f'{river.river_name}, main take out', place_type="take")