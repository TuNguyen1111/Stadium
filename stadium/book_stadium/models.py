from django.db import models
CHOICES = (
    ('admin', 'admin'),
    ('customer', 'customer')
)
# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=True, blank=False)
    phone_number = models.CharField(max_length=12, null=True, blank=False)
    role = models.CharField(max_length=20, null=True, choices=CHOICES)
    email = models.EmailField(max_length=100, null=True)

    def __str__(self):
        return self.name
    

class Stadium(models.Model):
    name = models.CharField(max_length=100, blank=False)
    address = models.CharField(max_length=100, null=True, blank=False)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    filed_count = models.IntegerField(blank=False)

    def __str__(self):
        return f'{self.name}-{self.address}'

class TimeFrame(models.Model):
    start_time = models.TimeField(blank=False)
    end_time = models.TimeField(blank=False)

    def __str__(self):
        return f'{self.start_time} - {self.end_time}'

class StadiumTimeFrame(models.Model):
    stadium = models.ForeignKey(Stadium, null=True, on_delete=models.SET_NULL)
    time_frame = models.ForeignKey(TimeFrame, null=True, on_delete=models.SET_NULL)
    price = models.IntegerField(blank=False)

    def __str__(self):
        return f'{self.stadium} - {self.time_frame}'

class Order(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    stadium_time_frame = models.ForeignKey(StadiumTimeFrame, null=True,on_delete=models.SET_NULL)
    field_number = models.IntegerField()
    order_datetime = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
    customer_phone_number = models.CharField(max_length=12)
    customer_name = models.CharField(max_length=100)

    def __str__(self):
        return f'Booked by {self.user}'