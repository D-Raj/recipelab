# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0013_auto_20150224_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='confidence_food',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='confidence_unit',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='conv_to_grams',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
