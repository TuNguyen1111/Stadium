from django.db import models

from .user import User
from .stadium import Stadium
from .common import Roles


class StarRatingPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    can_rate = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user}-{self.stadium}'

    @classmethod
    def create_user_rate_permission(cls, user, stadium):
        if user.role == Roles.PLAYER:
            user_permission_vote = StarRatingPermission.objects.create(
                    user=user, stadium=stadium)
        else:
            user_permission_vote = StarRatingPermission.objects.create(
                user=user, stadium=stadium, can_rate=False)
        user_permission_vote.save()
