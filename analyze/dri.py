# -*- coding: utf-8 -*-

from collections import OrderedDict

from analyze.models import Target, TargetSource, Nutrients, nut_def_pk2fields
from sr17.models import NUTR_DEF

"""
Daily nutrition recommendations from (2015-01-01):
    http://fnic.nal.usda.gov/dietary-guidance/dietary-reference-intakes/dri-tables

And for energy, using "Dietary Reference Intakes for Energy, Carbohydrate, Fiber, Fat, Fatty Acids, Cholesterol, Protein and Amino Acids" (2002)
    https://www.iom.edu/Reports/2002/Dietary-Reference-Intakes-for-Energy-Carbohydrate-Fiber-Fat-Fatty-Acids-Cholesterol-Protein-and-Amino-Acids.aspx
Warning: the energy targets need to be adjusted for age according to the following formula:
    Subtract 10 kcal/d for males and 7 kcal/d for females for each year of age above 19 years.

Using simple data structure instead of django models.  Usage:

>>> dri['Males']['19-30y']['copper']
900
>>> print dri_nutrients['copper']
µg
"""

# Encode microgram (with greek mu)  -- no need anymore as we're setting the encoding at the top of the file
# mug = u'\u00b5g'


# WARNING: SR27 uses "International Units" for Vitamins A and D.
# Need to translate the Targets somehow...
#
# From http://dietarysupplementdatabase.usda.nih.gov/ingredient_calculator/equation.php
#
# To convert Vitamin A as retinol:
#    From IU to mcg:  IU * 0.3 = mcg
#    From mcg to IU: mcg / 0.3 = IU
#
# To convert Vitamin A as beta-carotene:
#    From IU to mcg:  IU * 0.6 = mcg
#    From mcg to IU: mcg / 0.6 = IU
#
# To convert Vitamin D:
#    From IU to mcg: IU * 0.025 = mcg
#    For example: 400 IU * 0.025 = 10 mcg
#    From mcg to IU: mcg / 0.025 =IU
#
# so Vitamin A is the problem.  The DRI footnotes has this to say about their Vitamin A target:
#     As retinol activity equivalents (RAEs). 1 RAE = 1 μg retinol, 12 μg β-carotene, 24 μg α-carotene,
#     or 24 μg β-cryptoxanthin. The RAE for dietary provitamin A carotenoids is two-fold greater than retinol equivalents (RE),
#     whereas the RAE for preformed vitamin A is the same as RE.
#
# These ratios are not the same!
#

# Warning, some of these are in different units than SR27 - see the conversion data lower down
dri_nutrients =	OrderedDict([
    ("vitamin_a_rae", u"µg"),
    ("vitamin_c", "mg"),
    ("vitamin_d", u"µg"),
    ("vitamin_e", "mg"),
    ("vitamin_k", u"µg"),
    ("thiamin", "mg"),
    ("riboflavin", "mg"),
    ("niacin", "mg"),
    ("vitamin_b6", "mg"),
    ("folate", u"µg"),
    ("vitamin_b12", u"µg"),
    ("pantothenic_acid", "mg"),
    ("biotin", u"µg"),
    ("choline", "mg"),

    ("calcium", "mg"),
    ("chromium", u"µg"),
    ("copper", u"µg"),
    ("fluoride", "mg"),
    ("iodine", u"µg"),
    ("iron", "mg"),
    ("magnesium", "mg"),
    ("manganese", "mg"),
    ("molybdenum", u"µg"),
    ("phosphorus", "mg"),
    ("selenium", u"µg"),
    ("zinc", "mg"),
    ("potassium", "g"),
    ("sodium", "g"),
    ("chloride", "g"),

    ("water", "L"),
    ("carbohydrate", "g"),
    ("fiber", "g"),
    ("fat", "g"),
    ("linoleic_acid", "g"),
    ("alpha_linoleic_acid", "g"),
    ("protein", "g"),

    ("energy", "kcal"),
#    ("fat", "g"),
])

dri_nutrients_convert_to_sr27 = {
    "copper": 0.001,       # DRI µg => SR27 mg
    "fluoride": 1000.0,    # DRI mg => SR27 µg
    "potassium": 1000.0,   # DRI g  => SR27 mg
    "sodium": 1000.0,      # DRI g  => SR27 mg
    "vitamin_d": 40.0,     # DRI µg => SR27 IU
    "water": 1000.0,       # DRI L  => SR27 g
}

# The values from 0 to 8 years are all the same for male/female except for energy and fat.
dri = {
    "Males": {
        "0to6mo": {
            'values': [ 400, 40, 10, 4, 2.0, 0.2, 0.3, 2, 0.1, 65, 0.4, 1.7, 5, 125,
                        200, 0.2, 200, 0.01, 110, 0.27, 30, 0.003, 2, 100, 15, 2, 0.4, 0.12, 0.18,
                        0.7, 60, None, 31, 4.4, 0.5, 9.1,
                        570, ],
            'age_min': 0.0,
            'age_max': 0.5,
        },
        "6to12mo": {
            'values': [ 500, 50, 10, 5, 2.5, 0.3, 0.4, 4, 0.3, 80, 0.5, 1.8, 6, 150,
                        260, 5.5, 220, 0.5, 130, 11, 75, 0.6, 3, 275, 20, 3, 0.7, 0.37, 0.57,
                        0.8, 95, None, 30, 4.6, 0.5, 11.0,
                        743, ],
            'age_min': 0.5,
            'age_max': 1.0,
        },
        "1-3y": {
            'values': [ 300,  15,  15, 6, 30, 0.5, 0.5, 6, 0.5, 150, 0.9, 2, 8, 200,
                        700, 11, 340, 0.7, 90, 7, 80, 1.2, 17, 460, 20, 3, 3.0, 1.0, 1.5,
                        1.3, 130, 19, None, 7, 0.7, 13,
                        1046, ],
            'age_min': 1.0,
            'age_max': 4.0,
        },
        "4-8y": {
            'values': [ 400, 25, 15, 7, 55, 0.6, 0.6, 8, 0.6, 200, 1.2, 3, 12, 250,
                        1000, 15, 440, 1, 90, 10, 130, 1.5, 22, 500, 30, 5, 3.8, 1.2, 1.9,
                        1.7, 130, 25, None, 10, 0.9, 19,
                        1742, ],
            'age_min': 4.0,
            'age_max': 9.0,
        },
        "9-13y": {
            'values': [ 600, 45, 15, 11, 60, 0.9, 0.9, 12, 1.0, 300, 1.8, 4, 20, 375,
                        1300, 25, 700, 2, 120, 8, 240, 1.9, 34, 1250, 40, 8, 4.5, 1.5, 2.3,
                        2.4, 130, 31, None, 12, 1.2, 34,
                        2279, ],
            'age_min': 9.0,
            'age_max': 14.0,
        },
        "14-18y": {
            'values': [ 900, 75, 15, 15, 75, 1.2, 1.3, 16, 1.3, 400, 2.4, 5, 25, 550,
                        1300, 35, 890, 3, 150, 11, 410, 2.2, 43, 1250, 55, 11, 4.7, 1.5, 2.3,
                        3.3, 130, 38, None, 16, 1.6, 52,
                        3152, ],
            'age_min': 14.0,
            'age_max': 19.0,
        },
        "19-30y": {
            'values': [ 900, 90, 15, 15, 120, 1.2, 1.3, 16, 1.3, 400, 2.4, 5, 30, 550,
                        1000, 35, 900, 4, 150, 8, 400, 2.3, 45, 700, 55, 11, 4.7, 1.5, 2.3,
                        3.7, 130, 38, None, 17, 1.6, 56,
                        3067, ],
            'age_min': 19.0,
            'age_max': 31.0,
        },
        "31-50y": {
            'values': [ 900, 90, 15, 15, 120, 1.2, 1.3, 16, 1.3, 400, 2.4, 5, 30, 550,
                        1000, 35, 900, 4, 150, 8, 420, 2.3, 45, 700, 55, 11, 4.7, 1.5, 2.3,
                        3.7, 130, 38, None, 17, 1.6, 56,
                        3067, ],
            'age_min': 31.0,
            'age_max': 51.0,
        },
        "51-70y": {
            'values': [ 900, 90, 15, 15, 120, 1.2, 1.3, 16, 1.7, 400, 2.4, 5, 30, 550,
                        1000, 30, 900, 4, 150, 8, 420, 2.3, 45, 700, 55, 11, 4.7, 1.3, 2.0,
                        3.7, 130, 30, None, 14, 1.6, 56,
                        3067, ],
            'age_min': 51.0,
            'age_max': 71.0,
        },
        ">70y": {
            'values': [ 900, 90, 20, 15, 120, 1.2, 1.3, 16, 1.7, 400, 2.4, None, 5, 30, 550,
                        1200, 30, 900, 4, 150, 8, 420, 2.3, 45, 700, 55, 11, 4.7, 1.2, 1.8,
                        3.7, 130, 30, None, 14, 1.6, 56,
                        3067, ],
            'age_min': 71.0,
            'age_max': 500.0,
        },
    },
    "Females": {
        "0to6mo": {
            'values': [ 400, 40, 10, 4, 2.0, 0.2, 0.3, 2, 0.1, 65, 0.4, 1.7, 5, 125,
                        200, 0.2, 200, 0.01, 110, 0.27, 30, 0.003, 2, 100, 15, 2, 0.4, 0.12, 0.18,
                        0.7, 60, None, 31, 4.4, 0.5, 9.1,
                        520, ],
            'age_min': 0.0,
            'age_max': 0.5,
        },
        "6to12mo": {
            'values': [ 500, 50, 10, 5, 2.5, 0.3, 0.4, 4, 0.3, 80, 0.5, 1.8, 6, 150,
                        260, 5.5, 220, 0.5, 130, 11, 75, 0.6, 3, 275, 20, 3, 0.7, 0.37, 0.57,
                        0.8, 95, None, 30, 4.6, 0.5, 11.0,
                        676, ],
            'age_min': 0.5,
            'age_max': 1.0,
        },
        "1-3y": {
            'values': [ 300,  15,  15, 6, 30, 0.5, 0.5, 6, 0.5, 150, 0.9, 2, 8, 200,
                        700, 11, 340, 0.7, 90, 7, 80, 1.2, 17, 460, 20, 3, 3.0, 1.0, 1.5,
                        1.3, 130, 19, None, 7, 0.7, 13,
                        992, ],
            'age_min': 1.0,
            'age_max': 4.0,
        },
        "4-8y": {
            'values': [ 400, 25, 15, 7, 55, 0.6, 0.6, 8, 0.6, 200, 1.2, 3, 12, 250,
                        1000, 15, 440, 1, 90, 10, 130, 1.5, 22, 500, 30, 5, 3.8, 1.2, 1.9,
                        1.7, 130, 25, None, 10, 0.9, 19,
                        1642, ],
            'age_min': 4.0,
            'age_max': 9.0,
        },
        "9-13y": {
            'values': [ 600, 45, 15, 11, 60, 0.9, 0.9, 12, 1.0, 300, 1.8, 4, 20, 375,
                        1300, 21, 700, 2, 120, 8, 240, 1.6, 34, 1250, 40, 8, 4.5, 1.5, 2.3,
                        2.1, 130, 26, None, 10, 1.0, 34,
                        2071, ],
            'age_min': 9.0,
            'age_max': 14.0,
        },
        "14-18y": {
            'values': [ 700, 65, 15, 15, 75, 1.0, 1.0, 14, 1.2, 400, 2.4, 5, 25, 400,
                        1300, 24, 890, 3, 150, 15, 360, 1.6, 43, 1250, 55, 9, 4.7, 1.5, 2.3,
                        2.3, 130, 26, None, 11, 1.1, 46,
                        2368, ],
            'age_min': 14.0,
            'age_max': 19.0,
        },
        "19-30y": {
            'values': [ 700, 75, 15, 15, 90, 1.1, 1.1, 14, 1.3, 400, 2.4, 5, 30, 425,
                        1000, 25, 900, 3, 150, 18, 310, 1.8, 45, 700, 55, 8, 4.7, 1.5, 2.3,
                        2.7, 130, 25, None, 12, 1.1, 46,
                        2403, ],
            'age_min': 19.0,
            'age_max': 31.0,
        },
        "31-50y": {
            'values': [ 700, 75, 15, 15, 90, 1.1, 1.1, 14, 1.3, 400, 2.4, 5, 30, 425,
                        1000, 25, 900, 3, 150, 18, 320, 1.8, 45, 700, 55, 8, 4.7, 1.5, 2.3,
                        2.7, 130, 25, None, 12, 1.1, 46,
                        2403, ],
            'age_min': 31.0,
            'age_max': 51.0,
        },
        "51-70y": {
            'values': [ 700, 75, 15, 15, 90, 1.1, 1.1, 14, 1.5, 400, 2.4, None, 5, 30,
                        425, 1200, 20, 900, 3, 150, 8, 320, 1.8, 45, 700, 55, 8, 4.7, 1.3,
                        2.0, 2.7, 130, 21, None, 11, 1.1, 46,
                        2403, ],
            'age_min': 51.0,
            'age_max': 71.0,
        },
        ">70y": {
            'values': [ 700, 75, 20, 15, 90, 1.1, 1.1, 14, 1.5, 400, 2.4, 5, 30, 425,
                        1200, 20, 900, 3, 150, 8, 320, 1.8, 45, 700, 55, 8, 4.7, 1.2, 1.8,
                        2.7, 130, 21, None, 11, 1.1, 46,
                        2403, ],
            'age_min': 71.0,
            'age_max': 500.0,
        },
    },
    "Pregnancy": {
        "14-18y": {
            'values': [ 750, 80, 15, 15, 75, 1.4, 1.4, 18, 1.9, 600, 2.6, 6, 30, 450,
                        1300, 29, 1000, 3, 220, 27, 400, 2.0, 50, 1250, 60, 12, 4.7, 1.5, 2.3,
                        3.0, 175, 28, None, 13, 1.4, 71,
                        2708, ],
            'age_min': 14.0,
            'age_max': 19.0,
        },
        "19-30y": {
            'values': [ 770, 85, 15, 15, 90, 1.4, 1.4, 18, 1.9, 600, 2.6, 6, 30, 450,
                        1000, 30, 1000, 3, 220, 27, 350, 2.0, 50, 700, 60, 11, 4.7, 1.5, 2.3,
                        3.0, 175, 28, None, 13, 1.4, 71,
                        2743, ],
            'age_min': 19.0,
            'age_max': 31.0,
        },
        "31-50y": {
            'values': [ 770, 85, 15, 15, 90, 1.4, 1.4, 18, 1.9, 600, 2.6, 6, 30, 450,
                        1000, 30, 1000, 3, 220, 27, 360, 2.0, 50, 700, 60, 11, 4.7, 1.5, 2.3,
                        3.0, 175, 28, None, 13, 1.4, 71,
                        2743, ],
            'age_min': 31.0,
            'age_max': 51.0,
        },
    },
    "Lactation": {
        "14-18y": {
            'values': [ 1200, 115, 15, 19, 75, 1.4, 1.6, 17, 2.0, 500, 2.8, 7, 35, 550,
                        1300, 44, 1300, 3, 290, 10, 360, 2.6, 50, 1250, 70, 13, 5.1, 1.5, 2.3,
                        3.8, 210, 29, None, 13, 1.3, 71,
                        2768, ],
            'age_min': 14.0,
            'age_max': 19.0,
        },
        "19-30y": {
            'values': [ 1300, 120, 15, 19, 90, 1.4, 1.6, 17, 2.0, 500, 2.8, 7, 35, 550,
                        1000, 45, 1300, 3, 290, 9, 310, 2.6, 50, 700, 70, 12, 5.1, 1.5, 2.3,
                        3.8, 210, 29, None, 13, 1.3, 71,
                        2803, ],
            'age_min': 19.0,
            'age_max': 31.0,
        },
        "31-50y": {
            'values': [ 1300, 120, 15, 19, 90, 1.4, 1.6, 17, 2.0, 500, 2.8, 7, 35, 550,
                        1000, 45, 1300, 3, 290, 9, 320, 2.6, 50, 700, 70, 12, 5.1, 1.5, 2.3,
                        3.8, 210, 29, None, 13, 1.3, 71,
                        2803, ],
            'age_min': 31.0,
            'age_max': 51.0,
        },
    },
}

#############################################################################################################################################################

tolerable_nutrients = OrderedDict([
    ("vitamin_a_rae", u"µg"),
    ("vitamin_c", "mg"),
    ("vitamin_d", u"µg"),
    ("vitamin_e", "mg"),
    ("vitamin_k", u"µg"),
    ("thiamin", "mg"),
    ("riboflavin", "mg"),
    ("niacin", "mg"),
    ("vitamin_b6", "mg"),
    ("folate", u"µg"),
    ("vitamin_b12", u"µg"),
    ("pantothenic_acid", "mg"),
    ("biotin", u"µg"),
    ("choline", "g"),
    ("carotenoids", u"µg"),

    ("arsenic", u"µg"),
    ("boron", "mg"),
    ("calcium", "mg"),
    ("chromium", u"µg"),
    ("copper", u"µg"),
    ("fluoride", "mg"),
    ("iodine", u"µg"),
    ("iron", "mg"),
    ("magnesium", "mg"),
    ("manganese", "mg"),
    ("molybdenum", u"µg"),
    ("nickel", "mg"),
    ("phosphorus", "g"),
    ("selenium", u"µg"),
    ("silicon", u"µg"),
    ("vanadium", "mg"),
    ("zinc", "mg"),
    ("sodium", "g"),
    ("chloride", "g"),
])

def find_sr27_incompatibility(nutrient_list):
    """
    Pass in either tolerable_nutrients or dri_nutrients, and get a useful list of incompatibilities with SR27:
        find_sr27_incompatibility(tolerable_nutrients)
        find_sr27_incompatibility(dri_nutrients)
    """
    d = {}
    for k, v in nut_def_pk2fields.iteritems():
        # Get pk in NUTR_DEF table for each field_name
        d[v['field_name']] = k

    for k, v in nutrient_list.iteritems():
        if not k in d.keys():
            print 'NOT FOUND IN SR27: ' + k
            continue
        n = NUTR_DEF.objects.get(pk=d[k])
        if v != n.Units:
            print '        ' + k + '   DRI Unit: ' + v + '   SR27 Unit: ' + n.Units


tolerable_nutrients_convert_to_sr27 = {
    "copper": 0.001,       # DRI µg  => SR27 mg
    "fluoride": 1000.0,    # DRI mg  => SR27 µg
    "sodium": 1000.0,      # DRI g   => SR27 mg
    "vitamin_d": 40.0,     # DRI µg  => SR27 IU
    "choline": 1000.0,     # DRI g   => SR27 mg
    "phosphorus": 1000.0,  # DRI g   => SR27 mg
}

tolerable = {
    "Infants": {
        "0to6mo": {
            'values': [ 600,None,25,None,None,None,None,None,None,None,None,None,None,None,None,None,None,1000,None,None,0.7,None,40,None,None,None,None,None,45,None,None,4,None,None ],
            'age_min': 0.0,
            'age_max': 0.5,
        },
        "6to12mo": {
            'values': [ 600,None,38,None,None,None,None,None,None,None,None,None,None,None,None,None,None,1500,None,None,0.9,None,40,None,None,None,None,None,60,None,None,5,None,None ],
            'age_min': 0.5,
            'age_max': 1.0,
        },
    },
    "Children": {
        "1-3y": {
            'values': [ 600,400,63,200,None,None,None,10,30,300,None,None,None,1.0,None,None,3,2500,None,1000,1.3,200,40,65,2,300,0.2,3,90,None,None,7,1.5,2.3 ],
            'age_min': 1.0,
            'age_max': 4.0,
        },
        "4-8y": {
            'values': [ 900,650,75,300,None,None,None,15,40,400,None,None,None,1.0,None,None,6,2500,None,3000,2.2,300,40,110,3,600,0.3,3,150,None,None,12,1.9,2.9 ],
            'age_min': 4.0,
            'age_max': 9.0,
        },
    },
    "Males": {
        "9-13y": {
            'values': [ 1700,1200,100,600,None,None,None,20,60,600,None,None,None,2.0,None,None,11,3000,None,5000,10,600,40,350,6,1100,0.6,4,280,None,None,23,2.2,3.4 ],
            'age_min': 9.0,
            'age_max': 14.0,
        },
        "14-18y": {
            'values': [ 2800,1800,100,800,None,None,None,30,80,800,None,None,None,3.0,None,None,17,3000,None,8000,10,900,45,350,9,1700,1.0,4,400,None,None,34,2.3,3.6 ],
            'age_min': 14.0,
            'age_max': 19.0,
        },
        "19-30y": {
            'values': [ 3000,2000,100,1000,None,None,None,35,100,1000,None,None,None,3.5,None,None,20,2500,None,10000,10,1100,45,350,11,2000,1.0,4,400,None,1.8,40,2.3,3.6 ],
            'age_min': 19.0,
            'age_max': 31.0,
        },
        "31-50y": {
            'values': [ 3000,2000,100,1000,None,None,None,35,100,1000,None,None,None,3.5,None,None,20,2500,None,10000,10,1100,45,350,11,2000,1.0,4,400,None,1.8,40,2.3,3.6 ],
            'age_min': 31.0,
            'age_max': 51.0,
        },
        "51-70y": {
            'values': [ 3000,2000,100,1000,None,None,None,35,100,1000,None,None,None,3.5,None,None,20,2000,None,10000,10,1100,45,350,11,2000,1.0,4,400,None,1.8,40,2.3,3.6 ],
            'age_min': 51.0,
            'age_max': 70.0,
        },
        ">70y": {
            'values': [ 3000,2000,100,1000,None,None,None,35,100,1000,None,None,None,3.5,None,None,20,2000,None,10000,10,1100,45,350,11,2000,1.0,3,400,None,1.8,40,2.3,3.6 ],
            'age_min': 70.0,
            'age_max': 500.0,
        },
    },
    "Females": {
        "9-13y": {
            'values': [ 1700,1200,100,600,None,None,None,20,60,600,None,None,None,2.0,None,None,11,3000,None,5000,10,600,40,350,6,1100,0.6,4,280,None,None,23,2.2,3.4 ],
            'age_min': 9.0,
            'age_max': 14.0,
        },
        "14-18y": {
            'values': [ 2800,1800,100,800,None,None,None,30,80,800,None,None,None,3.0,None,None,17,3000,None,8000,10,900,45,350,9,1700,1.0,4,400,None,None,34,2.3,3.6 ],
            'age_min': 14.0,
            'age_max': 19.0,
        },
        "19-30y": {
            'values': [ 3000,2000,100,1000,None,None,None,35,100,1000,None,None,None,3.5,None,None,20,2500,None,10000,10,1100,45,350,11,2000,1.0,4,400,None,1.8,40,2.3,3.6 ],
            'age_min': 19.0,
            'age_max': 31.0,
        },
        "31-50y": {
            'values': [ 3000,2000,100,1000,None,None,None,35,100,1000,None,None,None,3.5,None,None,20,2500,None,10000,10,1100,45,350,11,2000,1.0,4,400,None,1.8,40,2.3,3.6 ],
            'age_min': 31.0,
            'age_max': 51.0,
        },
        "51-70y": {
            'values': [ 3000,2000,100,1000,None,None,None,35,100,1000,None,None,None,3.5,None,None,20,2000,None,10000,10,1100,45,350,11,2000,1.0,4,400,None,1.8,40,2.3,3.6 ],
            'age_min': 51.0,
            'age_max': 70.0,
        },
        ">70y": {
            'values': [ 3000,2000,100,1000,None,None,None,35,100,1000,None,None,None,3.5,None,None,20,2000,None,10000,10,1100,45,350,11,2000,1.0,3,400,None,1.8,40,2.3,3.6 ],
            'age_min': 70.0,
            'age_max': 500.0,
        },
    },
    "Pregnancy": {
        "14-18y": {
            'values': [ 2800,1800,100,800,None,None,None,30,80,800,None,None,None,3.0,None,None,17,3000,None,8000,10,900,45,350,9,1700,1.0,3.5,400,None,None,34,2.3,3.6 ],
            'age_min': 14.0,
            'age_max': 19.0,
        },
        "19-30y": {
            'values': [ 3000,2000,100,1000,None,None,None,35,100,1000,None,None,None,3.5,None,None,20,2500,None,10000,10,1100,45,350,11,2000,1.0,3.5,400,None,None,40,2.3,3.6 ],
            'age_min': 19.0,
            'age_max': 31.0,
        },
        "31-50y": {
            'values': [ 3000,2000,100,1000,None,None,None,35,100,1000,None,None,None,3.5,None,None,20,2500,None,10000,10,1100,45,350,11,2000,1.0,3.5,400,None,None,40,2.3,3.6 ],
            'age_min': 31.0,
            'age_max': 50.0,
        },
    },
    "Lactation": {
        "14-18y": {
            'values': [ 2800,1800,100,800,None,None,None,30,80,800,None,None,None,3.0,None,None,17,3000,None,8000,10,900,45,350,9,1700,1.0,4,400,None,None,34,2.3,3.6 ],
            'age_min': 14.0,
            'age_max': 19.0,
        },
        "19-30y": {
            'values': [ 3000,2000,100,1000,None,None,None,35,100,1000,None,None,None,3.5,None,None,20,2500,None,10000,10,1100,45,350,11,2000,1.0,4,400,None,None,40,2.3,3.6 ],
            'age_min': 19.0,
            'age_max': 31.0,
        },
        "31-50y": {
            'values': [ 3000,2000,100,1000,None,None,None,35,100,1000,None,None,None,3.5,None,None,20,2500,None,10000,10,1100,45,350,11,2000,1.0,4,400,None,None,40,2.3,3.6 ],
            'age_min': 31.0,
            'age_max': 50.0,
        },
    },
}

def create_targets():
    """
    This is a function you run just once to convert the data structures in this module into Django models, and store them in the Target table.
    Any nutrient given in units other than SR27's units will be converted!
    """
    DBG = False


    nut_def_pk2fields

    def tmp(title, type, dri_fields_dict, value_dict, conv_dict):
        source = TargetSource()
        source.name = title
        source.save()
        if DBG:
            print '--------------- ' + title + ' ---------------'
        for k1, v1 in value_dict.iteritems():
            subcategory = k1
            for k2, v2 in v1.iteritems():
                t = Target()
                t.source = source
                t.type = type
                t.category = k1
                t.age_group = k2
                t.age_min = v2['age_min']
                t.age_max = v2['age_max']

                if DBG:
                    print "---------------------------------------------------------------------------"
                    print "Type:" + t.type + " Subcategory:" + t.subcategory + " Age-Group:" + t.age_group

                v3 = v2['values']
                d = dict(zip(dri_fields_dict.keys(), v3))
                if DBG:
                    print v3
                    print d
                n = Nutrients()
                nutrient_fields = n._meta.get_all_field_names()
                for f in d:
#                    unit = d[f]
                    if f in nutrient_fields and d[f] is not None:
                        # Handle unit conversion where required!!!
                        target = d[f] * conv_dict.get(f, 1.0)

                        if DBG:
                            print f + ' = ' + str(target)
                        else:
                            setattr(n, f, target)
                    else:
                        print 'Warning: ' + f + " doesn't exist in SR27"
                if not DBG:
                    t.save()
                    n.target = t
                    n.save()

    tmp('USDA Recommended Dietary Allowances and Adequate Intakes', 'min', dri_nutrients, dri, dri_nutrients_convert_to_sr27)
    tmp('USDA Tolerable Upper Intake Levels', 'max', tolerable_nutrients, tolerable, tolerable_nutrients_convert_to_sr27)


def delete_targets():
    targets = Target.objects.all()
    for t in targets:
        nn = t.nutrients_set.all()
        for n in nn:
            n.delete()
        t.delete()
