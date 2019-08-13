# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sr17', '0005_auto_20150312_0054'),
    ]

    operations = [
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(help_text=b'Top-level category, can be description of official data source or user-defined (e.g.: Daily maximum tolerable nutrients', max_length=255)),
                ('subcategory', models.CharField(help_text=b'Sub-category (e.g.: Male, or Lactation', max_length=255, null=True, blank=True)),
                ('age_group', models.CharField(help_text=b'A human-readable description of the age range (e.g.: 0 to 6 months)', max_length=255)),
                ('type', models.CharField(max_length=3, choices=[(b'min', b'minimum'), (b'avg', b'average'), (b'max', b'maximum')])),
                ('age_min', models.FloatField(help_text=b'Minimum age for this group, in years', null=True, blank=True)),
                ('age_max', models.FloatField(help_text=b'Maximum age for this group, in years', null=True, blank=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='nutrients',
            name='target',
            field=models.ForeignKey(blank=True, to='sr17.Target', null=True),
            preserve_default=True,
        ),
    ]
