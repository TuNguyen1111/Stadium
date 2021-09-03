from django.db import models


class TimeFrame(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.start_time} - {self.end_time}'
