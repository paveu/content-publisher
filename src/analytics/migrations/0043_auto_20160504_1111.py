# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-04 11:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0042_auto_20160504_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageview',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 4, 11, 11, 6, 706055, tzinfo=utc)),
        ),
    ]
