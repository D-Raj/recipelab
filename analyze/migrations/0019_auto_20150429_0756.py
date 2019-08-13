# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0018_auto_20150429_0756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='target',
            name='source',
            field=models.ForeignKey(to='analyze.TargetSource'),
            preserve_default=True,
        ),
    ]
