# Generated by Django 3.0.2 on 2020-01-20 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20200119_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='instruments_practiced',
            field=models.ManyToManyField(to='app.Instrument'),
        ),
    ]
