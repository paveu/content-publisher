# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0015_category_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='order',
            field=models.PositiveIntegerField(default=1),
            preserve_default=True,
        ),
    ]
