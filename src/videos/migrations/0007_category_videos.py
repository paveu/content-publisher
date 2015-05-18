# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_remove_video_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='videos',
            field=models.ManyToManyField(to='videos.Video', null=True, blank=True),
            preserve_default=True,
        ),
    ]
