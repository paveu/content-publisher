# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pageview',
            name='timestamp',
            field=models.DateField(default=datetime.datetime(2015, 3, 29, 11, 51, 22, 690207, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
