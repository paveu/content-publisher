# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0017_auto_20150329_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='share_message',
            field=models.TextField(default=b'Check out this awesome video.'),
            preserve_default=True,
        ),
    ]
