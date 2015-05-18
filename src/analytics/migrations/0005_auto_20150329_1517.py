# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0004_auto_20150329_1245'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pageview',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AlterField(
            model_name='pageview',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 29, 15, 17, 1, 198009, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
