# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0012_auto_20150223_2248'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='user_edited',
            new_name='user_verified',
        ),
    ]
