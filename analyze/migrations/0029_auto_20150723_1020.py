# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0028_auto_20150723_0736'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='subscription_expiry',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='status',
            field=models.CharField(default=b'trial', max_length=3, choices=[(b'try', b'trial'), (b'sub', b'subscribed'), (b'dea', b'deactivated'), (b'gue', b'guest')]),
            preserve_default=True,
        ),
    ]
