# Generated by Django 3.1.7 on 2021-05-18 09:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(default='', max_length=100)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('phone_number', models.CharField(blank=True, max_length=12)),
                ('role', models.CharField(choices=[('owner', 'Chủ sân'), ('player', 'Người đặt')], default='player', max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Stadium',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('field_count', models.PositiveSmallIntegerField()),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='book_stadium')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TimeFrame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='StadiumTimeFrame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('is_open', models.BooleanField(default=True)),
                ('stadium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_stadium.stadium')),
                ('time_frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_stadium.timeframe')),
            ],
        ),
        migrations.AddField(
            model_name='stadium',
            name='time_frames',
            field=models.ManyToManyField(through='book_stadium.StadiumTimeFrame', to='book_stadium.TimeFrame'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField(default=django.utils.timezone.now)),
                ('field_numbers', models.JSONField(blank=True, null=True)),
                ('pitch_clothes', models.BooleanField(blank=True, default=False)),
                ('type_stadium', models.CharField(choices=[('7players', 'Sân 7'), ('11players', 'Sân 11')], default='7players', max_length=30)),
                ('order_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_accepted', models.BooleanField(default=False)),
                ('customer_phone_number', models.CharField(blank=True, max_length=12)),
                ('customer_name', models.CharField(blank=True, max_length=100)),
                ('stadium_time_frame', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='book_stadium.stadiumtimeframe')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=1000)),
                ('star_point', models.IntegerField(blank=True, null=True)),
                ('stadium', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='book_stadium.stadium')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
