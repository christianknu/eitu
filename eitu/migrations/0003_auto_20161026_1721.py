# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-26 15:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eitu', '0002_auto_20161026_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occupancy',
            name='timestamp',
            field=models.CharField(max_length=255),
        ),
    ]