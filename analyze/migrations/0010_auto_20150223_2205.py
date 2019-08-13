# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0009_auto_20150216_0051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='weight',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 23, 22, 5, 21, 610464), auto_now=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ingredient',
            name='user_edited',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='recipe',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 23, 22, 5, 21, 609778), auto_now=True),
            preserve_default=True,
        ),
    ]
