# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-26 14:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Occupancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=255)),
                ('occupancy', models.IntegerField()),
                ('timestamp', models.DateField()),
            ],
        ),
    ]