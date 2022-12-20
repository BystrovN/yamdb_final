from rest_framework.exceptions import ValidationError
from datetime import date


def validate_title_year(year):
    if year > date.today().year:
        raise ValidationError('Год выпуска не может быть больше текущего')
