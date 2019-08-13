# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='steps',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
