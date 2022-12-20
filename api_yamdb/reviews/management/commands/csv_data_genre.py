import csv

from django.core.management import BaseCommand
from reviews.models import Genre


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('static/data/genre.csv') as f:
            table = csv.reader(f)
            next(table)
            for column in table:
                if not Genre.objects.filter(
                    pk=column[0], name=column[1], slug=column[2]
                ).exists():
                    genre = Genre(
                        pk=column[0], name=column[1], slug=column[2]
                    )
                    genre.save()
