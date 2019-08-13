# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0010_auto_20150223_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='updated',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='recipe',
            name='updated',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
    ]
