# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0023_auto_20160422_2008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='desc',
        ),
        migrations.AddField(
            model_name='video',
            name='description',
            field=models.TextField(max_length=5000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
