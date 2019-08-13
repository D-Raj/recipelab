# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0003_auto_20150202_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='recipe',
            field=models.ForeignKey(blank=True, to='analyze.Recipe', null=True),
            preserve_default=True,
        ),
    ]
