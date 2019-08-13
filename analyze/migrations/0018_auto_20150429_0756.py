# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0017_auto_20150429_0702'),
    ]

    operations = [
        migrations.CreateModel(
            name='TargetSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Name of official data source, or "User-Defined"', max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='target',
            name='source',
            field=models.ForeignKey(blank=True, to='analyze.TargetSource', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='target',
            name='title',
            field=models.CharField(help_text=b'User specified name for this target', max_length=255),
            preserve_default=True,
        ),
    ]
