# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0027_userprofile_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='status',
            field=models.CharField(default=b'try', max_length=3, choices=[(b'try', b'trial'), (b'sub', b'subscribed'), (b'dea', b'deactivated')]),
            preserve_default=True,
        ),
    ]
