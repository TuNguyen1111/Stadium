# Generated by Django 3.1.7 on 2021-04-06 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_stadium', '0030_auto_20210406_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]
