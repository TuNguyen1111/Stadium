from django.db import models

from .user import User
from .stadium import Stadium


class StarRatingPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    can_rate = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user}-{self.stadium}'
