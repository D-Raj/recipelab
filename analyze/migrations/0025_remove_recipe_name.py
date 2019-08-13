# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0022_userprofile_age'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='name',
        ),
    ]
