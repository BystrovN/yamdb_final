import csv

from django.core.management import BaseCommand

from reviews.models import Comment, Review, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('static/data/comments.csv') as f:
            table = csv.reader(f)
            next(table)
            for column in table:
                if not Comment.objects.filter(
                    pk=column[0], author=column[3], pub_date=column[4]
                ).exists():
                    comment = Comment(
                        pk=column[0],
                        review=Review.objects.get(id=column[1]),
                        text=column[2],
                        author=User.objects.get(id=column[3]),
                        pub_date=column[4],
                    )
                    comment.save()
