# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0016_auto_20150316_1104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='target',
            name='subcategory',
        ),
        migrations.AddField(
            model_name='target',
            name='title',
            field=models.CharField(default=b'User-defined', help_text=b'Description of official data source or user-defined (e.g.: Daily maximum tolerable nutrients', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='target',
            name='category',
            field=models.CharField(help_text=b'Category (e.g.: Male, or Lactation', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
