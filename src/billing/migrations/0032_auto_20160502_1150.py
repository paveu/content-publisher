# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-02 11:50
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0031_auto_20160502_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='date_end',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 2, 11, 50, 20, 304081, tzinfo=utc), verbose_name=b'End Date'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='date_start',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 2, 11, 50, 20, 304001, tzinfo=utc), verbose_name=b'Start Date'),
        ),
    ]
