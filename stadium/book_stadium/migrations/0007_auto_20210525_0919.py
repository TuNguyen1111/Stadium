# Generated by Django 3.1.7 on 2021-05-25 02:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book_stadium', '0006_auto_20210521_1457'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stadium',
            options={'ordering': ['-pk']},
        ),
    ]
