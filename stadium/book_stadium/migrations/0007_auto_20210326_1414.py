# Generated by Django 3.1.7 on 2021-03-26 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_stadium', '0006_auto_20210326_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=12),
        ),
    ]
