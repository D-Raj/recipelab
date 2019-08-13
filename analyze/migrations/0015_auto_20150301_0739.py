# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0014_auto_20150301_0735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='sr17',
            field=models.ForeignKey(blank=True, to='sr17.FOOD_DES', null=True),
            preserve_default=True,
        ),
    ]
