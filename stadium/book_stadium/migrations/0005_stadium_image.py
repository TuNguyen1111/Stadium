# Generated by Django 3.1.7 on 2021-03-26 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_stadium', '0004_auto_20210325_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='stadium',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='book_stadium'),
        ),
    ]
