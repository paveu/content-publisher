# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_video_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='free_preview',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
