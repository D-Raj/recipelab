# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sr17', '0006_auto_20150312_0232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nutrients',
            name='sr17',
        ),
        migrations.RemoveField(
            model_name='nutrients',
            name='target',
        ),
        migrations.DeleteModel(
            name='Nutrients',
        ),
        migrations.RemoveField(
            model_name='target',
            name='user',
        ),
        migrations.DeleteModel(
            name='Target',
        ),
    ]
