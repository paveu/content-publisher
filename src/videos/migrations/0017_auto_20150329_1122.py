# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0016_video_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ['order', '-timestamp']},
        ),
    ]
