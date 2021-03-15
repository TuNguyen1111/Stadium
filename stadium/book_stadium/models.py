from django.db import models
from django.contrib.auth.models import AbstractUser


class Roles(models.TextChoices):
    OWNER = 'owner', 'Chủ sân'
    PLAYER = 'player', 'Người đặt'

# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.CharField(max_length=20, choices=Roles.choices)

    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.username


class Stadium(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    field_count = models.PositiveSmallIntegerField()
    time_frames = models.ManyToManyField('TimeFrame', through='StadiumTimeFrame')

    def __str__(self):
        return f'{self.name}-{self.address}'


class TimeFrame(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.start_time} - {self.end_time}'


class StadiumTimeFrame(models.Model):
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    time_frame = models.ForeignKey(TimeFrame, on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.stadium} - {self.time_frame}'


class Order(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    stadium_time_frame = models.ForeignKey(StadiumTimeFrame, null=True, on_delete=models.SET_NULL)
    field_number = models.PositiveSmallIntegerField()
    order_datetime = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField()
    customer_phone_number = models.CharField(max_length=12)
    customer_name = models.CharField(max_length=100)

    def __str__(self):
        return f'Booked by {self.user}'
