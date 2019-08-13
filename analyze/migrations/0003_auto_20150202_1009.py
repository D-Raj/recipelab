# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0002_recipe_steps'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='conv_factor',
            new_name='conv_to_grams',
        ),
    ]
