# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('analytics', '0003_auto_20150329_1218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pageview',
            name='count',
        ),
        migrations.AddField(
            model_name='pageview',
            name='primary_content_type',
            field=models.ForeignKey(related_name='primary_obj', blank=True, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pageview',
            name='primary_object_id',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pageview',
            name='secondary_content_type',
            field=models.ForeignKey(related_name='secondary_obj', blank=True, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pageview',
            name='secondary_object_id',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pageview',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 29, 12, 45, 4, 837022, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
