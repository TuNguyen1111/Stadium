from django.db import models

from .user import User
from .stadiumtimeframe import StadiumTimeFrame
from .common import TypeOfStadium

from django.utils import timezone


class Order(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    # ngay dat san cua user
    order_date = models.DateField(default=timezone.now)

    # dat khung gio nao
    stadium_time_frame = models.ForeignKey(
        StadiumTimeFrame, null=True, on_delete=models.SET_NULL)
    field_numbers = models.JSONField(blank=True, null=True)
    pitch_clothes = models.BooleanField(default=False, blank=True)
    type_stadium = models.CharField(
        max_length=30, choices=TypeOfStadium.choices, default=TypeOfStadium.SMALL)

    # ngay bat dau dat san cua user
    order_datetime = models.DateTimeField(default=timezone.now)

    is_accepted = models.BooleanField(default=False)
    customer_phone_number = models.CharField(max_length=12, blank=True)
    customer_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'Booked by {self.customer_name}'
