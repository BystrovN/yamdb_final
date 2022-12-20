import csv

from django.core.management import BaseCommand
from reviews.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('static/data/users.csv') as f:
            table = csv.reader(f)
            next(table)
            for column in table:
                if not User.objects.filter(username=column[1]).exists():
                    user = User(
                        pk=column[0],
                        username=column[1],
                        email=column[2],
                        role=column[3],
                        bio=column[4],
                        first_name=column[5],
                        last_name=column[6],
                    )
                    user.save()
