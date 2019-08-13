# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import analyze.models


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0030_auto_20160108_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='target',
            field=models.ForeignKey(default=analyze.models.get_default_target, to='analyze.Target'),
        ),
    ]
