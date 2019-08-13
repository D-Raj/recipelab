# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sr17', '0007_auto_20150316_1104'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('analyze', '0015_auto_20150301_0739'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nutrients',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('protein', models.FloatField(null=True, blank=True)),
                ('fat', models.FloatField(null=True, blank=True)),
                ('carbohydrate', models.FloatField(null=True, blank=True)),
                ('ash', models.FloatField(null=True, blank=True)),
                ('energy', models.FloatField(null=True, blank=True)),
                ('starch', models.FloatField(null=True, blank=True)),
                ('sucrose', models.FloatField(null=True, blank=True)),
                ('glucose', models.FloatField(null=True, blank=True)),
                ('fructose', models.FloatField(null=True, blank=True)),
                ('lactose', models.FloatField(null=True, blank=True)),
                ('maltose', models.FloatField(null=True, blank=True)),
                ('alcohol', models.FloatField(null=True, blank=True)),
                ('water', models.FloatField(null=True, blank=True)),
                ('adjusted_protein', models.FloatField(null=True, blank=True)),
                ('caffeine', models.FloatField(null=True, blank=True)),
                ('theobromine', models.FloatField(null=True, blank=True)),
                ('energy_kj', models.FloatField(null=True, blank=True)),
                ('sugars_total', models.FloatField(null=True, blank=True)),
                ('galactose', models.FloatField(null=True, blank=True)),
                ('fiber', models.FloatField(null=True, blank=True)),
                ('calcium', models.FloatField(null=True, blank=True)),
                ('iron', models.FloatField(null=True, blank=True)),
                ('magnesium', models.FloatField(null=True, blank=True)),
                ('phosphorus', models.FloatField(null=True, blank=True)),
                ('potassium', models.FloatField(null=True, blank=True)),
                ('sodium', models.FloatField(null=True, blank=True)),
                ('zinc', models.FloatField(null=True, blank=True)),
                ('copper', models.FloatField(null=True, blank=True)),
                ('fluoride', models.FloatField(null=True, blank=True)),
                ('manganese', models.FloatField(null=True, blank=True)),
                ('selenium', models.FloatField(null=True, blank=True)),
                ('vitamin_a', models.FloatField(null=True, blank=True)),
                ('retinol', models.FloatField(null=True, blank=True)),
                ('vitamin_a_rae', models.FloatField(null=True, blank=True)),
                ('carotene_beta', models.FloatField(null=True, blank=True)),
                ('carotene_alpha', models.FloatField(null=True, blank=True)),
                ('vitamin_e', models.FloatField(null=True, blank=True)),
                ('vitamin_d', models.FloatField(null=True, blank=True)),
                ('vitamin_d2', models.FloatField(null=True, blank=True)),
                ('vitamin_d3', models.FloatField(null=True, blank=True)),
                ('vitamin_d2_d3', models.FloatField(null=True, blank=True)),
                ('cryptoxanthin_beta', models.FloatField(null=True, blank=True)),
                ('lycopene', models.FloatField(null=True, blank=True)),
                ('lutein_zeaxanthin', models.FloatField(null=True, blank=True)),
                ('tocopherol_beta', models.FloatField(null=True, blank=True)),
                ('tocopherol_gamma', models.FloatField(null=True, blank=True)),
                ('tocopherol_delta', models.FloatField(null=True, blank=True)),
                ('tocotrienol_alpha', models.FloatField(null=True, blank=True)),
                ('tocotrienol_beta', models.FloatField(null=True, blank=True)),
                ('tocotrienol_gamma', models.FloatField(null=True, blank=True)),
                ('tocotrienol_delta', models.FloatField(null=True, blank=True)),
                ('vitamin_c', models.FloatField(null=True, blank=True)),
                ('thiamin', models.FloatField(null=True, blank=True)),
                ('riboflavin', models.FloatField(null=True, blank=True)),
                ('niacin', models.FloatField(null=True, blank=True)),
                ('pantothenic_acid', models.FloatField(null=True, blank=True)),
                ('vitamin_b6', models.FloatField(null=True, blank=True)),
                ('folate', models.FloatField(null=True, blank=True)),
                ('vitamin_b12', models.FloatField(null=True, blank=True)),
                ('choline', models.FloatField(null=True, blank=True)),
                ('menaquinone_4', models.FloatField(null=True, blank=True)),
                ('dihydrophylloquinone', models.FloatField(null=True, blank=True)),
                ('vitamin_k', models.FloatField(null=True, blank=True)),
                ('folic_acid', models.FloatField(null=True, blank=True)),
                ('folate_food', models.FloatField(null=True, blank=True)),
                ('folate_dfe', models.FloatField(null=True, blank=True)),
                ('betaine', models.FloatField(null=True, blank=True)),
                ('tryptophan', models.FloatField(null=True, blank=True)),
                ('threonine', models.FloatField(null=True, blank=True)),
                ('isoleucine', models.FloatField(null=True, blank=True)),
                ('leucine', models.FloatField(null=True, blank=True)),
                ('lysine', models.FloatField(null=True, blank=True)),
                ('methionine', models.FloatField(null=True, blank=True)),
                ('cystine', models.FloatField(null=True, blank=True)),
                ('phenylalanine', models.FloatField(null=True, blank=True)),
                ('tyrosine', models.FloatField(null=True, blank=True)),
                ('valine', models.FloatField(null=True, blank=True)),
                ('arginine', models.FloatField(null=True, blank=True)),
                ('histidine', models.FloatField(null=True, blank=True)),
                ('alanine', models.FloatField(null=True, blank=True)),
                ('aspartic_acid', models.FloatField(null=True, blank=True)),
                ('glutamic_acid', models.FloatField(null=True, blank=True)),
                ('glycine', models.FloatField(null=True, blank=True)),
                ('proline', models.FloatField(null=True, blank=True)),
                ('serine', models.FloatField(null=True, blank=True)),
                ('hydroxyproline', models.FloatField(null=True, blank=True)),
                ('vitamin_e_added', models.FloatField(null=True, blank=True)),
                ('vitamin_b12_added', models.FloatField(null=True, blank=True)),
                ('cholesterol', models.FloatField(null=True, blank=True)),
                ('trans_fatty_acids', models.FloatField(null=True, blank=True)),
                ('saturated_fatty_acids', models.FloatField(null=True, blank=True)),
                ('f4d0', models.FloatField(null=True, blank=True)),
                ('f6d0', models.FloatField(null=True, blank=True)),
                ('f8d0', models.FloatField(null=True, blank=True)),
                ('f10d0', models.FloatField(null=True, blank=True)),
                ('f12d0', models.FloatField(null=True, blank=True)),
                ('f14d0', models.FloatField(null=True, blank=True)),
                ('f16d0', models.FloatField(null=True, blank=True)),
                ('f18d0', models.FloatField(null=True, blank=True)),
                ('f20d0', models.FloatField(null=True, blank=True)),
                ('f18d1', models.FloatField(null=True, blank=True)),
                ('f18d2', models.FloatField(null=True, blank=True)),
                ('f18d3', models.FloatField(null=True, blank=True)),
                ('f20d4', models.FloatField(null=True, blank=True)),
                ('f22d6', models.FloatField(null=True, blank=True)),
                ('f22d0', models.FloatField(null=True, blank=True)),
                ('f14d1', models.FloatField(null=True, blank=True)),
                ('f16d1', models.FloatField(null=True, blank=True)),
                ('f18d4', models.FloatField(null=True, blank=True)),
                ('f20d1', models.FloatField(null=True, blank=True)),
                ('f20d5', models.FloatField(null=True, blank=True)),
                ('f22d1', models.FloatField(null=True, blank=True)),
                ('f22d5', models.FloatField(null=True, blank=True)),
                ('phytosterols', models.FloatField(null=True, blank=True)),
                ('stigmasterol', models.FloatField(null=True, blank=True)),
                ('campesterol', models.FloatField(null=True, blank=True)),
                ('beta_sitosterol', models.FloatField(null=True, blank=True)),
                ('monounsaturated_fatty_acids', models.FloatField(null=True, blank=True)),
                ('polyunsaturated_fatty_acids', models.FloatField(null=True, blank=True)),
                ('f15d0', models.FloatField(null=True, blank=True)),
                ('f17d0', models.FloatField(null=True, blank=True)),
                ('f24d0', models.FloatField(null=True, blank=True)),
                ('f16d1t', models.FloatField(null=True, blank=True)),
                ('f18d1t', models.FloatField(null=True, blank=True)),
                ('f22d1t', models.FloatField(null=True, blank=True)),
                ('f18d2t', models.FloatField(null=True, blank=True)),
                ('f18d2i', models.FloatField(null=True, blank=True)),
                ('f18d2tt', models.FloatField(null=True, blank=True)),
                ('f18d2cla', models.FloatField(null=True, blank=True)),
                ('f24d1c', models.FloatField(null=True, blank=True)),
                ('f20d2cn6', models.FloatField(null=True, blank=True)),
                ('f16d1c', models.FloatField(null=True, blank=True)),
                ('f18d1c', models.FloatField(null=True, blank=True)),
                ('f18d2cn6', models.FloatField(null=True, blank=True)),
                ('f22d1c', models.FloatField(null=True, blank=True)),
                ('f18d3cn6', models.FloatField(null=True, blank=True)),
                ('f17d1', models.FloatField(null=True, blank=True)),
                ('f20d3', models.FloatField(null=True, blank=True)),
                ('trans_monoenoic_fatty_acids', models.FloatField(null=True, blank=True)),
                ('trans_polyenoic_fatty_acids', models.FloatField(null=True, blank=True)),
                ('f13d0', models.FloatField(null=True, blank=True)),
                ('f15d1', models.FloatField(null=True, blank=True)),
                ('f18d3cn3', models.FloatField(null=True, blank=True)),
                ('f20d3n3', models.FloatField(null=True, blank=True)),
                ('f20d3n6', models.FloatField(null=True, blank=True)),
                ('f20d4n6', models.FloatField(null=True, blank=True)),
                ('f18d3i', models.FloatField(null=True, blank=True)),
                ('f21d5', models.FloatField(null=True, blank=True)),
                ('f22d4', models.FloatField(null=True, blank=True)),
                ('f18d1tn7', models.FloatField(null=True, blank=True)),
                ('sr17', models.ForeignKey(blank=True, to='sr17.FOOD_DES', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
            field=models.ForeignKey(blank=True, to='analyze.Target', null=True),
            preserve_default=True,
        ),
    ]
