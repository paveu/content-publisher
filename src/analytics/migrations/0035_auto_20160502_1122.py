# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-02 11:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0034_auto_20160430_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageview',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 2, 11, 22, 25, 138573, tzinfo=utc)),
        ),
    ]
