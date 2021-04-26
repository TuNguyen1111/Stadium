# Generated by Django 3.1.7 on 2021-04-26 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_stadium', '0041_auto_20210426_1019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='field_number',
        ),
        migrations.RemoveField(
            model_name='order',
            name='three_field_merge',
        ),
        migrations.RemoveField(
            model_name='order',
            name='three_field_merge_display',
        ),
        migrations.AddField(
            model_name='order',
            name='field_numbers',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
