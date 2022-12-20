import csv

from django.core.management import BaseCommand

from reviews.models import Category, Title


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('static/data/titles.csv') as f:
            table = csv.reader(f)
            next(table)
            for column in table:
                if not Title.objects.filter(
                    pk=column[0],
                    name=column[1],
                    year=column[2],
                    category=column[3],
                ).exists():
                    title = Title(
                        pk=column[0],
                        name=column[1],
                        year=column[2],
                        category=Category.objects.get(id=column[3]),
                    )
                    title.save()
