from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save

from sr17.models import FOOD_DES, WEIGHT

class Recipe(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    serves = models.PositiveSmallIntegerField(default=1)
    private = models.BooleanField(default=False, blank=True)
    steps = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.name

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, blank=True, null=True)
    quantity = models.FloatField()
    weight = models.ForeignKey(WEIGHT, blank=True, null=True)
    unit = models.CharField(max_length=255, blank=True, null=True)    # If we are using a unit for which there is no entry in the SR27 WEIGHT table, put it here
    sr17 = models.ForeignKey(FOOD_DES, blank=True, null=True)
    def __unicode__(self):
        return self.sr17.Long_Desc

class TargetSource(models.Model):
    name = models.CharField(max_length=255, help_text='Name of official data source, or "User-Defined"')
    def __unicode__(self):
        return self.name

# This model captures DRI targets
target_types = (
    ('min', 'minimum'),
    ('avg', 'average'),
    ('max', 'maximum'),
)
class Target(models.Model):
    source = models.ForeignKey(TargetSource)
    title = models.CharField(max_length=255, help_text='User specified name for this target')
    category = models.CharField(max_length=255, null=True, blank=True, help_text='Category (e.g.: Male, or Lactation')
    age_group = models.CharField(max_length=255, help_text='A human-readable description of the age range (e.g.: 0 to 6 months)')
    type = models.CharField(max_length=3, choices=target_types)
    user = models.ForeignKey(User, null=True, blank=True)
    age_min = models.FloatField(null=True, blank=True, help_text='Minimum age for this group, in years')
    age_max = models.FloatField(null=True, blank=True, help_text='Maximum age for this group, in years')
    def __unicode__(self):
        return unicode(self.title) + unicode(self.category) + ' ' + unicode(self.age_group)

def get_default_target():
    t = Target.objects.get(category="Females", age_group="19-30y", type="min")
    return t.pk

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    target = models.ForeignKey(Target, default=get_default_target)
    age = models.PositiveSmallIntegerField(default=30)  # The "age" used to calculate nutritional targets, may not be the age of user
    status = models.CharField(max_length=25, default='trial')
    subscription_expiry = models.DateTimeField(blank=True, null=True)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

class Nutrients(models.Model):
    sr17 = models.ForeignKey(FOOD_DES, null=True, blank=True)
    target = models.ForeignKey(Target, null=True, blank=True)
    protein = models.FloatField(blank=True,null=True)
    fat = models.FloatField(blank=True,null=True)
    carbohydrate = models.FloatField(blank=True,null=True)
    ash = models.FloatField(blank=True,null=True)
    energy = models.FloatField(blank=True,null=True)
    starch = models.FloatField(blank=True,null=True)
    sucrose = models.FloatField(blank=True,null=True)
    glucose = models.FloatField(blank=True,null=True)
    fructose = models.FloatField(blank=True,null=True)
    lactose = models.FloatField(blank=True,null=True)
    maltose = models.FloatField(blank=True,null=True)
    alcohol = models.FloatField(blank=True,null=True)
    water = models.FloatField(blank=True,null=True)
    adjusted_protein = models.FloatField(blank=True,null=True)
    caffeine = models.FloatField(blank=True,null=True)
    theobromine = models.FloatField(blank=True,null=True)
    energy_kj = models.FloatField(blank=True,null=True)
    sugars_total = models.FloatField(blank=True,null=True)
    galactose = models.FloatField(blank=True,null=True)
    fiber = models.FloatField(blank=True,null=True)
    calcium = models.FloatField(blank=True,null=True)
    iron = models.FloatField(blank=True,null=True)
    magnesium = models.FloatField(blank=True,null=True)
    phosphorus = models.FloatField(blank=True,null=True)
    potassium = models.FloatField(blank=True,null=True)
    sodium = models.FloatField(blank=True,null=True)
    zinc = models.FloatField(blank=True,null=True)
    copper = models.FloatField(blank=True,null=True)
    fluoride = models.FloatField(blank=True,null=True)
    manganese = models.FloatField(blank=True,null=True)
    selenium = models.FloatField(blank=True,null=True)
    vitamin_a = models.FloatField(blank=True,null=True)
    retinol = models.FloatField(blank=True,null=True)
    vitamin_a_rae = models.FloatField(blank=True,null=True)
    carotene_beta = models.FloatField(blank=True,null=True)
    carotene_alpha = models.FloatField(blank=True,null=True)
    vitamin_e = models.FloatField(blank=True,null=True)
    vitamin_d = models.FloatField(blank=True,null=True)
    vitamin_d2 = models.FloatField(blank=True,null=True)
    vitamin_d3 = models.FloatField(blank=True,null=True)
    vitamin_d2_d3 = models.FloatField(blank=True,null=True)
    cryptoxanthin_beta = models.FloatField(blank=True,null=True)
    lycopene = models.FloatField(blank=True,null=True)
    lutein_zeaxanthin = models.FloatField(blank=True,null=True)
    tocopherol_beta = models.FloatField(blank=True,null=True)
    tocopherol_gamma = models.FloatField(blank=True,null=True)
    tocopherol_delta = models.FloatField(blank=True,null=True)
    tocotrienol_alpha = models.FloatField(blank=True,null=True)
    tocotrienol_beta = models.FloatField(blank=True,null=True)
    tocotrienol_gamma = models.FloatField(blank=True,null=True)
    tocotrienol_delta = models.FloatField(blank=True,null=True)
    vitamin_c = models.FloatField(blank=True,null=True)
    thiamin = models.FloatField(blank=True,null=True)
    riboflavin = models.FloatField(blank=True,null=True)
    niacin = models.FloatField(blank=True,null=True)
    pantothenic_acid = models.FloatField(blank=True,null=True)
    vitamin_b6 = models.FloatField(blank=True,null=True)
    folate = models.FloatField(blank=True,null=True)
    vitamin_b12 = models.FloatField(blank=True,null=True)
    choline = models.FloatField(blank=True,null=True)
    menaquinone_4 = models.FloatField(blank=True,null=True)
    dihydrophylloquinone = models.FloatField(blank=True,null=True)
    vitamin_k = models.FloatField(blank=True,null=True)
    folic_acid = models.FloatField(blank=True,null=True)
    folate_food = models.FloatField(blank=True,null=True)
    folate_dfe = models.FloatField(blank=True,null=True)
    betaine = models.FloatField(blank=True,null=True)
    tryptophan = models.FloatField(blank=True,null=True)
    threonine = models.FloatField(blank=True,null=True)
    isoleucine = models.FloatField(blank=True,null=True)
    leucine = models.FloatField(blank=True,null=True)
    lysine = models.FloatField(blank=True,null=True)
    methionine = models.FloatField(blank=True,null=True)
    cystine = models.FloatField(blank=True,null=True)
    phenylalanine = models.FloatField(blank=True,null=True)
    tyrosine = models.FloatField(blank=True,null=True)
    valine = models.FloatField(blank=True,null=True)
    arginine = models.FloatField(blank=True,null=True)
    histidine = models.FloatField(blank=True,null=True)
    alanine = models.FloatField(blank=True,null=True)
    aspartic_acid = models.FloatField(blank=True,null=True)
    glutamic_acid = models.FloatField(blank=True,null=True)
    glycine = models.FloatField(blank=True,null=True)
    proline = models.FloatField(blank=True,null=True)
    serine = models.FloatField(blank=True,null=True)
    hydroxyproline = models.FloatField(blank=True,null=True)
    vitamin_e_added = models.FloatField(blank=True,null=True)
    vitamin_b12_added = models.FloatField(blank=True,null=True)
    cholesterol = models.FloatField(blank=True,null=True)
    trans_fatty_acids = models.FloatField(blank=True,null=True)
    saturated_fatty_acids = models.FloatField(blank=True,null=True)
    f4d0 = models.FloatField(blank=True,null=True)
    f6d0 = models.FloatField(blank=True,null=True)
    f8d0 = models.FloatField(blank=True,null=True)
    f10d0 = models.FloatField(blank=True,null=True)
    f12d0 = models.FloatField(blank=True,null=True)
    f14d0 = models.FloatField(blank=True,null=True)
    f16d0 = models.FloatField(blank=True,null=True)
    f18d0 = models.FloatField(blank=True,null=True)
    f20d0 = models.FloatField(blank=True,null=True)
    f18d1 = models.FloatField(blank=True,null=True)
    f18d2 = models.FloatField(blank=True,null=True)
    f18d3 = models.FloatField(blank=True,null=True)
    f20d4 = models.FloatField(blank=True,null=True)
    f22d6 = models.FloatField(blank=True,null=True)
    f22d0 = models.FloatField(blank=True,null=True)
    f14d1 = models.FloatField(blank=True,null=True)
    f16d1 = models.FloatField(blank=True,null=True)
    f18d4 = models.FloatField(blank=True,null=True)
    f20d1 = models.FloatField(blank=True,null=True)
    f20d5 = models.FloatField(blank=True,null=True)
    f22d1 = models.FloatField(blank=True,null=True)
    f22d5 = models.FloatField(blank=True,null=True)
    phytosterols = models.FloatField(blank=True,null=True)
    stigmasterol = models.FloatField(blank=True,null=True)
    campesterol = models.FloatField(blank=True,null=True)
    beta_sitosterol = models.FloatField(blank=True,null=True)
    monounsaturated_fatty_acids = models.FloatField(blank=True,null=True)
    polyunsaturated_fatty_acids = models.FloatField(blank=True,null=True)
    f15d0 = models.FloatField(blank=True,null=True)
    f17d0 = models.FloatField(blank=True,null=True)
    f24d0 = models.FloatField(blank=True,null=True)
    f16d1t = models.FloatField(blank=True,null=True)
    f18d1t = models.FloatField(blank=True,null=True)
    f22d1t = models.FloatField(blank=True,null=True)
    f18d2t = models.FloatField(blank=True,null=True)
    f18d2i = models.FloatField(blank=True,null=True)
    f18d2tt = models.FloatField(blank=True,null=True)
    f18d2cla = models.FloatField(blank=True,null=True)
    f24d1c = models.FloatField(blank=True,null=True)
    f20d2cn6 = models.FloatField(blank=True,null=True)
    f16d1c = models.FloatField(blank=True,null=True)
    f18d1c = models.FloatField(blank=True,null=True)
    f18d2cn6 = models.FloatField(blank=True,null=True)
    f22d1c = models.FloatField(blank=True,null=True)
    f18d3cn6 = models.FloatField(blank=True,null=True)
    f17d1 = models.FloatField(blank=True,null=True)
    f20d3 = models.FloatField(blank=True,null=True)
    trans_monoenoic_fatty_acids = models.FloatField(blank=True,null=True)
    trans_polyenoic_fatty_acids = models.FloatField(blank=True,null=True)
    f13d0 = models.FloatField(blank=True,null=True)
    f15d1 = models.FloatField(blank=True,null=True)
    f18d3cn3 = models.FloatField(blank=True,null=True)
    f20d3n3 = models.FloatField(blank=True,null=True)
    f20d3n6 = models.FloatField(blank=True,null=True)
    f20d4n6 = models.FloatField(blank=True,null=True)
    f18d3i = models.FloatField(blank=True,null=True)
    f21d5 = models.FloatField(blank=True,null=True)
    f22d4 = models.FloatField(blank=True,null=True)
    f18d1tn7 = models.FloatField(blank=True,null=True)


# Cleaned, user-friendly names for nutrients in NUTR_DEF table
# This is what we are using as field names, added to the FOOD_DES table
nut_def_pk2fields = {
    '203': { 'field_name': 'protein', 'human_name': 'Protein' },
    '204': { 'field_name': 'fat', 'human_name': 'Fat' },
    '205': { 'field_name': 'carbohydrate', 'human_name': 'Carbohydrate' },
    '207': { 'field_name': 'ash', 'human_name': 'Ash' },
    '208': { 'field_name': 'energy', 'human_name': 'Energy' },
    '209': { 'field_name': 'starch', 'human_name': 'Starch' },
    '210': { 'field_name': 'sucrose', 'human_name': 'Sucrose' },
    '211': { 'field_name': 'glucose', 'human_name': 'Glucose' },
    '212': { 'field_name': 'fructose', 'human_name': 'Fructose' },
    '213': { 'field_name': 'lactose', 'human_name': 'Lactose' },
    '214': { 'field_name': 'maltose', 'human_name': 'Maltose' },
    '221': { 'field_name': 'alcohol', 'human_name': 'Alcohol' },
    '255': { 'field_name': 'water', 'human_name': 'Water' },
    '257': { 'field_name': 'adjusted_protein', 'human_name': 'Adjusted Protein' },
    '262': { 'field_name': 'caffeine', 'human_name': 'Caffeine' },
    '263': { 'field_name': 'theobromine', 'human_name': 'Theobromine' },
    '268': { 'field_name': 'energy_kj', 'human_name': 'Energy' },
    '269': { 'field_name': 'sugars_total', 'human_name': 'Sugar' },
    '287': { 'field_name': 'galactose', 'human_name': 'Galactose' },
    '291': { 'field_name': 'fiber', 'human_name': 'Fiber' },
    '301': { 'field_name': 'calcium', 'human_name': 'Calcium' },
    '303': { 'field_name': 'iron', 'human_name': 'Iron' },
    '304': { 'field_name': 'magnesium', 'human_name': 'Magnesium' },
    '305': { 'field_name': 'phosphorus', 'human_name': 'Phosphorus' },
    '306': { 'field_name': 'potassium', 'human_name': 'Potassium' },
    '307': { 'field_name': 'sodium', 'human_name': 'Sodium' },
    '309': { 'field_name': 'zinc', 'human_name': 'Zinc' },
    '312': { 'field_name': 'copper', 'human_name': 'Copper' },
    '313': { 'field_name': 'fluoride', 'human_name': 'Fluoride' },
    '315': { 'field_name': 'manganese', 'human_name': 'Manganese' },
    '317': { 'field_name': 'selenium', 'human_name': 'Selenium' },
    '318': { 'field_name': 'vitamin_a', 'human_name': 'Vitamin A' },
    '319': { 'field_name': 'retinol', 'human_name': 'Retinol' },
    '320': { 'field_name': 'vitamin_a_rae', 'human_name': 'Vitamin A' },  # as retinol activity equivalent (RAE)
    '321': { 'field_name': 'carotene_beta', 'human_name': 'Carotene Beta' },
    '322': { 'field_name': 'carotene_alpha', 'human_name': 'Carotene Alpha' },
    '323': { 'field_name': 'vitamin_e', 'human_name': 'Vitamin E' },
    '324': { 'field_name': 'vitamin_d', 'human_name': 'Vitamin D' },
    '325': { 'field_name': 'vitamin_d2', 'human_name': 'Vitamin D2' },
    '326': { 'field_name': 'vitamin_d3', 'human_name': 'Vitamin D3' },
    '328': { 'field_name': 'vitamin_d2_d3', 'human_name': 'Vitamin D2 and D3' },
    '334': { 'field_name': 'cryptoxanthin_beta', 'human_name': 'Cryptoxanthin Beta' },
    '337': { 'field_name': 'lycopene', 'human_name': 'Lycopene' },
    '338': { 'field_name': 'lutein_zeaxanthin', 'human_name': 'Lutein Zeaxanthin' },
    '341': { 'field_name': 'tocopherol_beta', 'human_name': 'Tocopherol Beta' },
    '342': { 'field_name': 'tocopherol_gamma', 'human_name': 'Tocopherol Gamma' },
    '343': { 'field_name': 'tocopherol_delta', 'human_name': 'Tocopherol Delta' },
    '344': { 'field_name': 'tocotrienol_alpha', 'human_name': 'Tocotrienol Alpha' },
    '345': { 'field_name': 'tocotrienol_beta', 'human_name': 'Tocotrienol Beta' },
    '346': { 'field_name': 'tocotrienol_gamma', 'human_name': 'Tocotrienol Gamma' },
    '347': { 'field_name': 'tocotrienol_delta', 'human_name': 'Tocotrienol Delta' },
    '401': { 'field_name': 'vitamin_c', 'human_name': 'Vitamin C' },
    '404': { 'field_name': 'thiamin', 'human_name': 'Vitamin B1 (Thiamin)' },
    '405': { 'field_name': 'riboflavin', 'human_name': 'Vitamin B2 (Riboflavin)' },
    '406': { 'field_name': 'niacin', 'human_name': 'Vitamin B3 (Niacin)' },
    '410': { 'field_name': 'pantothenic_acid', 'human_name': 'Vitamin B5 (Pantothenic Acid)' },
    '415': { 'field_name': 'vitamin_b6', 'human_name': 'Vitamin B6' },
    '417': { 'field_name': 'folate', 'human_name': 'Vitamin B9 (Folate)' },
    '418': { 'field_name': 'vitamin_b12', 'human_name': 'Vitamin B12' },
    '421': { 'field_name': 'choline', 'human_name': 'Choline' },
    '428': { 'field_name': 'menaquinone_4', 'human_name': 'Menaquinone 4' },
    '429': { 'field_name': 'dihydrophylloquinone', 'human_name': 'Dihydrophylloquinone' },
    '430': { 'field_name': 'vitamin_k', 'human_name': 'Vitamin K' },
    '431': { 'field_name': 'folic_acid', 'human_name': 'Folic acid' },
    '432': { 'field_name': 'folate_food', 'human_name': 'Folate Food' },
    '435': { 'field_name': 'folate_dfe', 'human_name': 'Folate Dfe' },
    '454': { 'field_name': 'betaine', 'human_name': 'Betaine' },
    '501': { 'field_name': 'tryptophan', 'human_name': 'Tryptophan' },
    '502': { 'field_name': 'threonine', 'human_name': 'Threonine' },
    '503': { 'field_name': 'isoleucine', 'human_name': 'Isoleucine' },
    '504': { 'field_name': 'leucine', 'human_name': 'Leucine' },
    '505': { 'field_name': 'lysine', 'human_name': 'Lysine' },
    '506': { 'field_name': 'methionine', 'human_name': 'Methionine' },
    '507': { 'field_name': 'cystine', 'human_name': 'Cystine' },
    '508': { 'field_name': 'phenylalanine', 'human_name': 'Phenylalanine' },
    '509': { 'field_name': 'tyrosine', 'human_name': 'Tyrosine' },
    '510': { 'field_name': 'valine', 'human_name': 'Valine' },
    '511': { 'field_name': 'arginine', 'human_name': 'Arginine' },
    '512': { 'field_name': 'histidine', 'human_name': 'Histidine' },
    '513': { 'field_name': 'alanine', 'human_name': 'Alanine' },
    '514': { 'field_name': 'aspartic_acid', 'human_name': 'Aspartic Acid' },
    '515': { 'field_name': 'glutamic_acid', 'human_name': 'Glutamic Acid' },
    '516': { 'field_name': 'glycine', 'human_name': 'Glycine' },
    '517': { 'field_name': 'proline', 'human_name': 'Proline' },
    '518': { 'field_name': 'serine', 'human_name': 'Serine' },
    '521': { 'field_name': 'hydroxyproline', 'human_name': 'Hydroxyproline' },
    '573': { 'field_name': 'vitamin_e_added', 'human_name': 'Vitamin E added' },
    '578': { 'field_name': 'vitamin_b12_added', 'human_name': 'Vitamin B12 added' },
    '601': { 'field_name': 'cholesterol', 'human_name': 'Cholesterol' },
    '605': { 'field_name': 'trans_fatty_acids', 'human_name': 'Trans' },
    '606': { 'field_name': 'saturated_fatty_acids', 'human_name': 'Saturated' },
    '607': { 'field_name': 'f4d0', 'human_name': 'f4d0' },
    '608': { 'field_name': 'f6d0', 'human_name': 'f6d0' },
    '609': { 'field_name': 'f8d0', 'human_name': 'f8d0' },
    '610': { 'field_name': 'f10d0', 'human_name': 'f10d0' },
    '611': { 'field_name': 'f12d0', 'human_name': 'f12d0' },
    '612': { 'field_name': 'f14d0', 'human_name': 'f14d0' },
    '613': { 'field_name': 'f16d0', 'human_name': 'f16d0' },
    '614': { 'field_name': 'f18d0', 'human_name': 'f18d0' },
    '615': { 'field_name': 'f20d0', 'human_name': 'f20d0' },
    '617': { 'field_name': 'f18d1', 'human_name': 'f18d1' },
    '618': { 'field_name': 'f18d2', 'human_name': 'f18d2' },
    '619': { 'field_name': 'f18d3', 'human_name': 'f18d3' },
    '620': { 'field_name': 'f20d4', 'human_name': 'f20d4' },
    '621': { 'field_name': 'f22d6', 'human_name': 'f22d6' },
    '624': { 'field_name': 'f22d0', 'human_name': 'f22d0' },
    '625': { 'field_name': 'f14d1', 'human_name': 'f14d1' },
    '626': { 'field_name': 'f16d1', 'human_name': 'f16d1' },
    '627': { 'field_name': 'f18d4', 'human_name': 'f18d4' },
    '628': { 'field_name': 'f20d1', 'human_name': 'f20d1' },
    '629': { 'field_name': 'f20d5', 'human_name': 'f20d5' },
    '630': { 'field_name': 'f22d1', 'human_name': 'f22d1' },
    '631': { 'field_name': 'f22d5', 'human_name': 'f22d5' },
    '636': { 'field_name': 'phytosterols', 'human_name': 'Phytosterols' },
    '638': { 'field_name': 'stigmasterol', 'human_name': 'Stigmasterol' },
    '639': { 'field_name': 'campesterol', 'human_name': 'Campesterol' },
    '641': { 'field_name': 'beta_sitosterol', 'human_name': 'Beta_Sitosterol' },
    '645': { 'field_name': 'monounsaturated_fatty_acids', 'human_name': 'Mono-unsaturated' },
    '646': { 'field_name': 'polyunsaturated_fatty_acids', 'human_name': 'Poly-unsaturated' },
    '652': { 'field_name': 'f15d0', 'human_name': 'f15d0' },
    '653': { 'field_name': 'f17d0', 'human_name': 'f17d0' },
    '654': { 'field_name': 'f24d0', 'human_name': 'f24d0' },
    '662': { 'field_name': 'f16d1t', 'human_name': 'f16d1t' },
    '663': { 'field_name': 'f18d1t', 'human_name': 'f18d1t' },
    '664': { 'field_name': 'f22d1t', 'human_name': 'f22d1t' },
    '665': { 'field_name': 'f18d2t', 'human_name': 'f18d2t' },
    '666': { 'field_name': 'f18d2i', 'human_name': 'f18d2i' },
    '669': { 'field_name': 'f18d2tt', 'human_name': 'f18d2tt' },
    '670': { 'field_name': 'f18d2cla', 'human_name': 'f18d2cla' },
    '671': { 'field_name': 'f24d1c', 'human_name': 'f24d1c' },
    '672': { 'field_name': 'f20d2cn6', 'human_name': 'f20d2cn6' },
    '673': { 'field_name': 'f16d1c', 'human_name': 'f16d1c' },
    '674': { 'field_name': 'f18d1c', 'human_name': 'f18d1c' },
    '675': { 'field_name': 'f18d2cn6', 'human_name': 'f18d2cn6' },
    '676': { 'field_name': 'f22d1c', 'human_name': 'f22d1c' },
    '685': { 'field_name': 'f18d3cn6', 'human_name': 'f18d3cn6' },
    '687': { 'field_name': 'f17d1', 'human_name': 'f17d1' },
    '689': { 'field_name': 'f20d3', 'human_name': 'f20d3' },
    '693': { 'field_name': 'trans_monoenoic_fatty_acids', 'human_name': 'Trans Monoenoic Fatty Acids' },
    '695': { 'field_name': 'trans_polyenoic_fatty_acids', 'human_name': 'Trans Polyenoic Fatty Acids' },
    '696': { 'field_name': 'f13d0', 'human_name': 'f13d0' },
    '697': { 'field_name': 'f15d1', 'human_name': 'f15d1' },
    '851': { 'field_name': 'f18d3cn3', 'human_name': 'f18d3cn3' },
    '852': { 'field_name': 'f20d3n3', 'human_name': 'f20d3n3' },
    '853': { 'field_name': 'f20d3n6', 'human_name': 'f20d3n6' },
    '855': { 'field_name': 'f20d4n6', 'human_name': 'f20d4n6' },
    '856': { 'field_name': 'f18d3i', 'human_name': 'f18d3i' },
    '857': { 'field_name': 'f21d5', 'human_name': 'f21d5' },
    '858': { 'field_name': 'f22d4', 'human_name': 'f22d4' },
    '859': { 'field_name': 'f18d1tn7', 'human_name': 'f18d1tn7' },
}

def sr27_tabulate():
    """
    Run this one time only!
    The SR27 database structure links FOOD_DEScriptions to NUT_DATA which contains nutritional values but also
    complex statistical data about how those values were determined.  To simplify this structure, compile all the nutritional
    values into django Nutrients models and link them to their FOOD_DES models.
    """
    food_des = FOOD_DES.objects.all()
    num = len(food_des)
    count = 1
    for f in food_des:
        print "Processing " + str(count) + " of " + str(num)
        count += 1

        nutrients = {}
        for n in f.nut_data_set.all():
            k, v = (n.Nutr_No.Nutr_No, n.Nutr_Val)
            fname = nut_def_pk2fields[k]['field_name']
            nutrients[fname] = v
#            setattr(f, fname, v)  # instead of adding the nutrient fields to the FOOD_DES model, we now have a separate Nutrients table
#        f.save()
        nutrients['sr17'] = f
        n = Nutrients(**nutrients)
        n.save()




def get_weight_words():
    """
    This is a throw-away function to grab the first comma-sep word in the sr17 WEIGHT table entries
    """
    equivalences = WEIGHT.objects.all()
    words = {}
    for e in equivalences:
        t = e.Msre_Desc
        t = t.split(',')[0]  # Use only first comma-position
        t = t.split('(')[0]  # Ignore anything after opening parenthesis
        words[t] = None
    keys = words.keys()
    keys.sort()
    for k in keys:
        print k

