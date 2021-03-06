# Generated by Django 3.1.7 on 2021-05-21 07:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book_stadium', '0005_starrating_can_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='starrating',
            name='can_rate',
        ),
        migrations.CreateModel(
            name='StarRatingPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_rate', models.BooleanField(default=True)),
                ('stadium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_stadium.stadium')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
