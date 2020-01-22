# Generated by Django 3.0.2 on 2020-01-21 21:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import time


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailPreferences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('features', models.BooleanField(default=True)),
                ('practicing', models.BooleanField(default=True)),
                ('promotions', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('bpm_start', models.PositiveSmallIntegerField()),
                ('bpm_end', models.PositiveSmallIntegerField()),
                ('minutes', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Improvement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=128)),
                ('timestamp', models.FloatField(db_index=True, default=time.time)),
                ('payload_json', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Positive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Practice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('notes', models.TextField(blank=True, null=True)),
                ('exercises', models.ManyToManyField(to='app.Exercise')),
                ('goals', models.ManyToManyField(to='app.Goal')),
                ('improvements', models.ManyToManyField(to='app.Improvement')),
                ('instrument', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Instrument')),
                ('positives', models.ManyToManyField(to='app.Positive')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_confirmed', models.BooleanField(default=False)),
                ('email_preferences', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                        to='app.EmailPreferences')),
                ('instruments_practiced', models.ManyToManyField(to='app.Instrument')),
                ('notifications', models.ManyToManyField(to='app.Notification')),
                ('practices', models.ManyToManyField(to='app.Practice')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,
                                              to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(db_index=True, max_length=128)),
                ('description', models.CharField(max_length=128)),
                ('complete', models.BooleanField(default=False)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='practice',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Profile'),
        ),
        migrations.AddField(
            model_name='notification',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Profile'),
        ),
    ]
