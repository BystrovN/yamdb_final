from django.core import management
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Выгрузить данные из всех csv файлов'

    def handle(self, *args, **options):
        management.call_command('csv_data_users')
        management.call_command('csv_data_category')
        management.call_command('csv_data_genre')
        management.call_command('csv_data_titles')
        management.call_command('csv_data_genre_title')
        management.call_command('csv_data_review')
        management.call_command('csv_data_comments')
