from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class Roles(models.TextChoices):
    OWNER = 'owner', 'Chủ sân'
    PLAYER = 'player', 'Người đặt'


class TypeOfStadium(models.TextChoices):
    SMALL = '7players', 'Sân 7'
    BIG = '11players', 'Sân 11'

# Create your models here.


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.CharField(
        max_length=20, choices=Roles.choices, default='player')
    email = models.EmailField(_('email address'), blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        if self.username:
            return self.username
        else:
            return self.email

    def is_missing_information(self):
        return self.phone_number == '' or self.username == ''


class Stadium(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    field_count = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to="book_stadium",
                              default=None, null=True, blank=True)
    time_frames = models.ManyToManyField(
        'TimeFrame', through='StadiumTimeFrame')

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
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.time_frame}'


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


class StarRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    comment = models.TextField()
    star_point = models.PositiveSmallIntegerField(
        default=0, blank=True, null=True)

    def __str__(self):
        return f'Star rate of {self.user}'
