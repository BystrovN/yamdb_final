import csv

from django.core.management import BaseCommand

from reviews.models import Genre, GenreTitle, Title


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('static/data/genre_title.csv') as f:
            table = csv.reader(f)
            next(table)
            for column in table:
                if not GenreTitle.objects.filter(
                    pk=column[0],
                    title=Title.objects.get(id=column[1]),
                    genre=Genre.objects.get(id=column[2]),
                ).exists():
                    genre_title = GenreTitle(
                        pk=column[0],
                        title=Title.objects.get(id=column[1]),
                        genre=Genre.objects.get(id=column[2]),
                    )
                    genre_title.save()
