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
