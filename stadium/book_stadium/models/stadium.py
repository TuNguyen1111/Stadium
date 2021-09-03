from django.db import models

from .user import User


class Stadium(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    field_count = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to="book_stadium",
                              default=None, null=True, blank=True)
    time_frames = models.ManyToManyField(
        'TimeFrame', through='StadiumTimeFrame')

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return f'{self.name}-{self.address}'

    @classmethod
    def get_stadium_by_owner(cls, owner):
        return cls.objects.filter(owner=owner)

    @classmethod
    def get_first_stadium_of_owner(cls, owner):
        return cls.objects.filter(owner=owner).first()

    @classmethod
    def get_all_stadium(cls):
        return cls.objects.all()
