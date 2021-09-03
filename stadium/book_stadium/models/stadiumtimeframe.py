from django.db import models

from .stadium import Stadium
from .timeframe import TimeFrame


class StadiumTimeFrame(models.Model):
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    time_frame = models.ForeignKey(TimeFrame, on_delete=models.CASCADE)
    price = models.IntegerField()
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.time_frame}'
