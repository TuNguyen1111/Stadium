from django.db import models


class Roles(models.TextChoices):
    OWNER = 'owner', 'Chủ sân'
    PLAYER = 'player', 'Người đặt'


class TypeOfStadium(models.TextChoices):
    SMALL = '7players', 'Sân 7'
    BIG = '11players', 'Sân 11'
