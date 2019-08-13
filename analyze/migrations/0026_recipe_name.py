# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0025_remove_recipe_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='name',
            field=models.CharField(default='untitled', max_length=255),
            preserve_default=False,
        ),
    ]
