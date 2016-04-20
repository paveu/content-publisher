# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0018_auto_20150330_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='image',
            field=models.ImageField(null=True, upload_to=b'images/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='taggeditem',
            name='tag',
            field=models.SlugField(choices=[(b'python', b'python'), (b'django', b'django'), (b'css', b'css'), (b'bootstrap', b'bootstrap'), (b'music', b'music')]),
            preserve_default=True,
        ),
    ]
