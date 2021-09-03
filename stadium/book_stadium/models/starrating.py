from django.db import models

from .user import User
from .stadium import Stadium

class StarRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    comment = models.TextField()
    star_point = models.PositiveSmallIntegerField(
        default=0, blank=True, null=True)

    def __str__(self):
        return f'Star rate of {self.user}'

    @classmethod
    def get_star_rating_by_stadium(cls, stadium, order_by=None):
        qs = StarRating.objects.filter(stadium=stadium)
        if order_by:
            qs = qs.order_by(order_by)
        return qs

    @classmethod
    def create_user_star_rating(cls, user, stadium, comment, star_point):
        new_user_rate = cls.objects.create(user=user, stadium=stadium, comment=comment, star_point=star_point)
        new_user_rate.save()
        return new_user_rate
