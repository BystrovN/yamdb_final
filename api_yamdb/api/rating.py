from django.db.models import Sum
from django.shortcuts import get_object_or_404
from reviews.models import Review, Title


class Rating:
    """
    Для расчета и записи рейтинга.
    Методы класса вызываются при создании/редактировании/удалении
    отзыва на соответствущее произведение.
    """

    NUMBER_OF_DECIMALS = 1

    @classmethod
    def _rating_calculation(cls, title_id):
        reviews_count = Review.objects.filter(title__id=title_id).count()
        score_sum = Review.objects.filter(title__id=title_id).aggregate(
            Sum('score')
        )

        return round(
            score_sum['score__sum'] / reviews_count, cls.NUMBER_OF_DECIMALS
        )

    @classmethod
    def title_rating(cls, title_id):
        title = get_object_or_404(Title, id=title_id)
        title.rating = cls._rating_calculation(title_id)
        title.save()
