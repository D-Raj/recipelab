# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sr17', '0007_auto_20150316_1104'),
        ('analyze', '0019_auto_20150429_0756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='confidence_food',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='confidence_unit',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='conv_to_grams',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='description',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='line_number',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='user_verified',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='weight',
            field=models.ForeignKey(blank=True, to='sr17.WEIGHT', null=True),
            preserve_default=True,
        ),
    ]
