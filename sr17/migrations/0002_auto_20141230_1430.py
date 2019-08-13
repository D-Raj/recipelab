# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sr17', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data_src',
            name='Title',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
