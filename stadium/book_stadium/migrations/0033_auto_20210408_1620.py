# Generated by Django 3.1.7 on 2021-04-08 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_stadium', '0032_auto_20210408_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_accepted',
            field=models.BooleanField(default=False),
        ),
    ]
