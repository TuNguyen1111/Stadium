# Generated by Django 3.1.7 on 2021-03-26 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_stadium', '0010_auto_20210326_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('owner', 'Chủ sân'), ('player', 'Người đặt')], default='player', max_length=20),
        ),
    ]