# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0022_auto_20160422_1454'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='share_message',
            new_name='desc',
        ),
    ]
