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

    @classmethod
    def get_stadium_timeframe_by_conditions(cls, conditions, order_by=None):
        qs = cls.objects.filter(**conditions)
        if order_by:
            qs = qs.order_by(order_by)
        return qs

    @classmethod
    def create_stadium_timeframe(cls, stadium, timeframe):
        stadium_time_frame = StadiumTimeFrame.objects.create(
                stadium=stadium,
                time_frame=timeframe,
                price=300_000,
            )
        stadium_time_frame.save()
