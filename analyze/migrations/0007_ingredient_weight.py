# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sr17', '0003_auto_20150103_1419'),
        ('analyze', '0006_auto_20150204_0702'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='weight',
            field=models.ForeignKey(blank=True, to='sr17.WEIGHT', null=True),
            preserve_default=True,
        ),
    ]
