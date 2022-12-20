from datetime import date

from rest_framework.exceptions import ValidationError


def validate_title_year(year):
    if year > date.today().year:
        raise ValidationError('Год выпуска не может быть больше текущего')
