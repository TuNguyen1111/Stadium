from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Stadium, StarRatingPermission


@receiver(post_save, sender=User)
def create_user_rating_permission(sender, instance, created, **kwargs):
    if created:
        stadiums = Stadium.objects.all().select_related('owner')
        for stadium in stadiums:
            user_permissions = StarRatingPermission.objects.create(
                user=instance, stadium=stadium)
            user_permissions.save()
