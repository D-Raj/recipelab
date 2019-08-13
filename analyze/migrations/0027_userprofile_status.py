# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0026_recipe_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='status',
            field=models.CharField(default=b'tr', max_length=2, choices=[(b'tr', b'trial'), (b'ac', b'active'), (b'in', b'inactive')]),
            preserve_default=True,
        ),
    ]
