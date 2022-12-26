import csv

from django.core.management import BaseCommand
from reviews.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('static/data/category.csv') as f:
            table = csv.reader(f)
            next(table)
            for column in table:
                if not Category.objects.filter(slug=column[2]).exists():
                    category = Category(
                        pk=column[0], name=column[1], slug=column[2]
                    )
                    category.save()
