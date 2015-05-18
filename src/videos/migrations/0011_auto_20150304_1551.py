# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0010_auto_20150304_0851'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='slug',
            field=models.SlugField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='video',
            unique_together=set([('slug', 'category')]),
        ),
    ]
