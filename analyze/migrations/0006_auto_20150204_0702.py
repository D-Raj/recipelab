# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0005_auto_20150204_0549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(default=b'untitled', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
