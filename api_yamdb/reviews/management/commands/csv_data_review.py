import csv

from django.core.management import BaseCommand

from reviews.models import Review, Title, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('static/data/review.csv') as f:
            table = csv.reader(f)
            next(table)
            for column in table:
                if not Review.objects.filter(
                    pk=column[0],
                    title=Title.objects.get(id=column[1]),
                    text=column[2],
                    author=User.objects.get(id=column[3]),
                    score=column[4],
                    pub_date=column[5],
                ).exists():
                    review = Review(
                        pk=column[0],
                        title=Title.objects.get(id=column[1]),
                        text=column[2],
                        author=User.objects.get(id=column[3]),
                        score=column[4],
                        pub_date=column[5],
                    )
                    review.save()
