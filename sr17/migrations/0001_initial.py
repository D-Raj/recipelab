# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DATA_SRC',
            fields=[
                ('DataSrc_ID', models.CharField(max_length=6, serialize=False, primary_key=True)),
                ('Authors', models.CharField(max_length=255, null=True, blank=True)),
                ('Title', models.CharField(max_length=255)),
                ('Year', models.CharField(max_length=4, null=True, blank=True)),
                ('Journal', models.CharField(max_length=135, null=True, blank=True)),
                ('Vol_City', models.CharField(max_length=16, null=True, blank=True)),
                ('Issue_State', models.CharField(max_length=5, null=True, blank=True)),
                ('Start_Page', models.CharField(max_length=5, null=True, blank=True)),
                ('End_Page', models.CharField(max_length=5, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DATSRCLN',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('DataSrc_ID', models.ForeignKey(to='sr17.DATA_SRC')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DERIV_CD',
            fields=[
                ('Deriv_Cd', models.CharField(max_length=4, serialize=False, primary_key=True)),
                ('Deriv_Desc', models.CharField(max_length=120)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FD_GROUP',
            fields=[
                ('FdGrp_Cd', models.CharField(max_length=4, serialize=False, primary_key=True)),
                ('FdGrp_Desc', models.CharField(max_length=60)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FOOD_DES',
            fields=[
                ('NDB_No', models.CharField(max_length=5, serialize=False, primary_key=True)),
                ('Long_Desc', models.CharField(max_length=200)),
                ('Shrt_Desc', models.CharField(max_length=60)),
                ('ComName', models.CharField(max_length=100, null=True, blank=True)),
                ('ManufacName', models.CharField(max_length=65, null=True, blank=True)),
                ('Survey', models.CharField(max_length=1, null=True, blank=True)),
                ('Ref_desc', models.CharField(max_length=135, null=True, blank=True)),
                ('Refuse', models.IntegerField(null=True, blank=True)),
                ('SciName', models.CharField(max_length=65, null=True, blank=True)),
                ('N_Factor', models.FloatField(null=True, blank=True)),
                ('Pro_Factor', models.FloatField(null=True, blank=True)),
                ('Fat_Factor', models.FloatField(null=True, blank=True)),
                ('CHO_Factor', models.FloatField(null=True, blank=True)),
                ('FdGrp_Cd', models.ForeignKey(to='sr17.FD_GROUP')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FOOTNOTE',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Footnt_No', models.CharField(max_length=4)),
                ('Footnt_Typ', models.CharField(max_length=1)),
                ('Nutr_No', models.CharField(max_length=3, null=True, blank=True)),
                ('Footnt_Txt', models.CharField(max_length=200)),
                ('NDB_No', models.ForeignKey(to='sr17.FOOD_DES')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LANGDESC',
            fields=[
                ('Factor_Code', models.CharField(max_length=5, serialize=False, primary_key=True)),
                ('Description', models.CharField(max_length=140)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LANGUAL',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Factor_Code', models.ForeignKey(to='sr17.LANGDESC')),
                ('NDB_No', models.ForeignKey(to='sr17.FOOD_DES')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NUT_DATA',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Nutr_Val', models.FloatField()),
                ('Num_Data_Pts', models.FloatField()),
                ('Std_Error', models.FloatField(null=True, blank=True)),
                ('Add_Nutr_Mark', models.CharField(max_length=1, null=True, blank=True)),
                ('Num_Studies', models.IntegerField(null=True, blank=True)),
                ('Min', models.FloatField(null=True, blank=True)),
                ('Max', models.FloatField(null=True, blank=True)),
                ('DF', models.IntegerField(null=True, blank=True)),
                ('Low_EB', models.FloatField(null=True, blank=True)),
                ('Up_EB', models.FloatField(null=True, blank=True)),
                ('Stat_cmt', models.CharField(max_length=10, null=True, blank=True)),
                ('AddMod_Date', models.CharField(max_length=10, null=True, blank=True)),
                ('CC', models.CharField(max_length=1, null=True, blank=True)),
                ('Deriv_Cd', models.ForeignKey(blank=True, to='sr17.DERIV_CD', null=True)),
                ('NDB_No', models.ForeignKey(to='sr17.FOOD_DES')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NUTR_DEF',
            fields=[
                ('Nutr_No', models.CharField(max_length=3, serialize=False, primary_key=True)),
                ('Units', models.CharField(max_length=7)),
                ('Tagname', models.CharField(max_length=20, null=True, blank=True)),
                ('NutrDesc', models.CharField(max_length=60)),
                ('Num_Dec', models.CharField(max_length=1)),
                ('SR_Order', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SRC_CD',
            fields=[
                ('Src_Cd', models.CharField(max_length=2, serialize=False, primary_key=True)),
                ('SrcCd_Desc', models.CharField(max_length=60)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WEIGHT',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Seq', models.CharField(max_length=2)),
                ('Amount', models.FloatField()),
                ('Msre_Desc', models.CharField(max_length=84)),
                ('Gm_Wgt', models.FloatField()),
                ('Num_Data_Pts', models.IntegerField(null=True, blank=True)),
                ('Std_Dev', models.FloatField(null=True, blank=True)),
                ('NDB_No', models.ForeignKey(to='sr17.FOOD_DES')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='nut_data',
            name='Nutr_No',
            field=models.ForeignKey(to='sr17.NUTR_DEF'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='nut_data',
            name='Ref_NDB_No',
            field=models.ForeignKey(related_name='NUT_DATA_REF', blank=True, to='sr17.FOOD_DES', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='nut_data',
            name='Src_Cd',
            field=models.ForeignKey(to='sr17.SRC_CD'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datsrcln',
            name='NDB_No',
            field=models.ForeignKey(to='sr17.FOOD_DES'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datsrcln',
            name='Nutr_No',
            field=models.ForeignKey(to='sr17.NUTR_DEF'),
            preserve_default=True,
        ),
    ]
