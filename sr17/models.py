from django.db import models
from django.contrib.auth.models import User


###############################################################################################################
###############################################################################################################
#                    USDA National Nutrient Database for Standard Reference rel 27
###############################################################################################################
###############################################################################################################

class FD_GROUP(models.Model):
    FdGrp_Cd = models.CharField(max_length=4,primary_key=True)
    FdGrp_Desc = models.CharField(max_length=60)
    def __unicode__(self):
        return self.FdGrp_Desc
    class Meta:
        verbose_name = "FD_GROUP"
        ordering = ["FdGrp_Desc"]


class FOOD_DES(models.Model):
    NDB_No = models.CharField(max_length=5,primary_key=True)
    FdGrp_Cd = models.ForeignKey(FD_GROUP)
    Long_Desc = models.CharField(max_length=200)
    Shrt_Desc = models.CharField(max_length=60)
    ComName = models.CharField(max_length=100,blank=True,null=True)
    ManufacName = models.CharField(max_length=65,blank=True,null=True)
    Survey = models.CharField(max_length=1,blank=True,null=True)
    Ref_desc = models.CharField(max_length=135,blank=True,null=True)
    Refuse = models.IntegerField(blank=True,null=True)
    SciName = models.CharField(max_length=65,blank=True,null=True)
    N_Factor = models.FloatField(blank=True,null=True)
    Pro_Factor = models.FloatField(blank=True,null=True)
    Fat_Factor = models.FloatField(blank=True,null=True)
    CHO_Factor = models.FloatField(blank=True,null=True)
    def __unicode__(self):
        return self.Long_Desc
    class Meta:
        verbose_name = "FOOD_DES"
        ordering = ["Long_Desc"]

class LANGDESC(models.Model):
    Factor_Code = models.CharField(max_length=5,primary_key=True)
    Description = models.CharField(max_length=140)
    def __unicode__(self):
        return self.Description
    class Meta:
        verbose_name = "LANGDESC"
        ordering = ["Description"]

#This is a many-to-many link table
class LANGUAL(models.Model):
    NDB_No = models.ForeignKey(FOOD_DES)
    Factor_Code = models.ForeignKey(LANGDESC)
    def __unicode__(self):
        return self.Factor_Code
    class Meta:
        verbose_name = "LANGUAL"
        ordering = ["Factor_Code"]


class NUTR_DEF(models.Model):
    Nutr_No = models.CharField(max_length=3,primary_key=True)
    Units = models.CharField(max_length=7)
    Tagname = models.CharField(max_length=20,blank=True,null=True)
    NutrDesc = models.CharField(max_length=60)
    Num_Dec = models.CharField(max_length=1)
    SR_Order = models.IntegerField()
    def __unicode__(self):
        return self.NutrDesc
    class Meta:
        verbose_name = "NUTR_DEF"
        ordering = ["NutrDesc"]

class SRC_CD(models.Model):
    Src_Cd = models.CharField(max_length=2,primary_key=True)
    SrcCd_Desc = models.CharField(max_length=60)
    def __unicode__(self):
        return self.SrcCd_Desc
    class Meta:
        verbose_name = "SRC_CD"
        ordering = ["SrcCd_Desc"]

class DERIV_CD(models.Model):
    Deriv_Cd = models.CharField(max_length=4,primary_key=True)
    Deriv_Desc = models.CharField(max_length=120)
    def __unicode__(self):
        return self.Deriv_Desc
    class Meta:
        verbose_name = "DERIV_CD"
        ordering = ["Deriv_Desc"]

class WEIGHT(models.Model):
    NDB_No = models.ForeignKey(FOOD_DES)
    Seq = models.CharField(max_length=2)
    Amount = models.FloatField()
    Msre_Desc = models.CharField(max_length=84)
    Gm_Wgt = models.FloatField()
    Num_Data_Pts = models.IntegerField(blank=True,null=True)
    Std_Dev = models.FloatField(blank=True,null=True)
    def __unicode__(self):
        return self.Msre_Desc
    class Meta:
        verbose_name = "WEIGHT"
        ordering = ["Msre_Desc"]

class FOOTNOTE(models.Model):
    NDB_No = models.ForeignKey(FOOD_DES)
    Footnt_No = models.CharField(max_length=4)
    Footnt_Typ = models.CharField(max_length=1)
    Nutr_No = models.CharField(max_length=3,blank=True,null=True)
    Footnt_Txt = models.CharField(max_length=200)
    def __unicode__(self):
        return self.Footnt_Txt
    class Meta:
        verbose_name = "FOOTNOTE"

class NUT_DATA(models.Model):
    NDB_No = models.ForeignKey(FOOD_DES)
    Nutr_No = models.ForeignKey(NUTR_DEF)
    Nutr_Val = models.FloatField()
    Num_Data_Pts = models.FloatField()
    Std_Error = models.FloatField(blank=True,null=True)
    Src_Cd = models.ForeignKey(SRC_CD)
    Deriv_Cd = models.ForeignKey(DERIV_CD,blank=True,null=True)
    Ref_NDB_No = models.ForeignKey(FOOD_DES,blank=True,null=True,related_name='NUT_DATA_REF')
    Add_Nutr_Mark = models.CharField(max_length=1,blank=True,null=True)
    Num_Studies = models.IntegerField(blank=True,null=True)
    Min = models.FloatField(blank=True,null=True)
    Max = models.FloatField(blank=True,null=True)
    DF = models.IntegerField(blank=True,null=True)
    Low_EB = models.FloatField(blank=True,null=True)
    Up_EB = models.FloatField(blank=True,null=True)
    Stat_cmt = models.CharField(max_length=10,blank=True,null=True)
    AddMod_Date = models.CharField(max_length=10,blank=True,null=True)
    CC = models.CharField(max_length=1,blank=True,null=True)
    def __unicode__(self):
        return unicode(self.Nutr_Val)
    class Meta:
        verbose_name = "NUT_DATA"

class DATA_SRC(models.Model):
    DataSrc_ID = models.CharField(max_length=6,primary_key=True)
    Authors = models.CharField(max_length=255,blank=True,null=True)
    # Title is null in SR17 DATA_SRC.txt record D3356 - this contradicts the documentation
    Title = models.CharField(max_length=255,blank=True,null=True)
    Year = models.CharField(max_length=4,blank=True,null=True)
    Journal = models.CharField(max_length=135,blank=True,null=True)
    Vol_City = models.CharField(max_length=16,blank=True,null=True)
    Issue_State = models.CharField(max_length=5,blank=True,null=True)
    Start_Page = models.CharField(max_length=5,blank=True,null=True)
    End_Page = models.CharField(max_length=5,blank=True,null=True)
    def __unicode__(self):
        return unicode(self.DataSrc_ID) + ':' + unicode(self.Title)
    class Meta:
        verbose_name = "DATA_SRC"
        ordering = ["DataSrc_ID"]
        
# This is a three-way link table
# For any combination of NDB_No (food item) and Nutr_No (nutrient)
# it links to the data source.
class DATSRCLN(models.Model):
    NDB_No = models.ForeignKey(FOOD_DES)
    Nutr_No = models.ForeignKey(NUTR_DEF)
    DataSrc_ID = models.ForeignKey(DATA_SRC)
    class Meta:
        verbose_name = "DATSRCLN"


###################################################################################################################

