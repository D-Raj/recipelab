from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.http import JsonResponse, HttpResponse, Http404
from collections import OrderedDict
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

import json

from analyze.models import Recipe, Ingredient, nut_def_pk2fields, Target, UserProfile
from analyze.ingredient import *
from analyze.dri import dri_nutrients
from sr17.models import FOOD_DES, NUTR_DEF


RECIPE_FIELDS = ('name', 'serves', 'private', 'steps')
INGREDIENT_FIELDS = ('quantity', 'unit', 'sr17', 'weight', 'description')

# NOT USED!!!
DEFAULT_UNITS = ('gram', 'oz')

UI_NUM_FOOD_MATCHES = 20
FORCE_REFRESH_OF_OLD_INGREDIENTS = False

# USDA database includes an integer value for Refuse, e.g. 36 for raw Bananas means the mass is 36% peel
# But a home cook is unlikely to include the peel in the values entered
REFUSE_COMPENSATION = False

# http://www.nlm.nih.gov/medlineplus/ency/article/002222.htm
# http://en.wikipedia.org/wiki/Essential_amino_acid
# http://chriskresser.com/folate-vs-folic-acid
nutrition_display_layout = (
    'energy',
    'protein',
    'carbohydrate', (
        'fiber',
        'starch',
        'sugars_total',
    ),
    'fat', (
        'monounsaturated_fatty_acids',
        'polyunsaturated_fatty_acids',
        'saturated_fatty_acids',
        'trans_fatty_acids',
    ),
    'cholesterol',
    'Vitamins', (
        'vitamin_a_rae',    # Retinol Activity Equivalent, see comments in dri.py module.
        'thiamin',          # B1
        'riboflavin',       # B2
        'niacin',           # B3
        'pantothenic_acid', # B5
        'vitamin_b6',       # B6
                            # B7 (Biotin)???
        'folate',           # B9
        'vitamin_b12',      # B12
        'vitamin_c',
        'vitamin_d',
        'vitamin_e',
        'vitamin_k',
        # Additional
        'choline',

    ),
    'Minerals', (
        'calcium',
        'copper',
        'iron',
        'fluoride',
        'magnesium',
        'manganese',
        'phosphorus',
        'potassium',
        'selenium',
        'sodium',
        'zinc',
    ),
)


def get_default_userprofile():
    return UserProfile()


def adjust_energy(val, userprofile):
    """
    As per "Dietary Reference Intakes for Energy, Carbohydrate, Fiber, Fat, Fatty Acids, Cholesterol, Protein and Amino Acids" (2002)
        https://www.iom.edu/Reports/2002/Dietary-Reference-Intakes-for-Energy-Carbohydrate-Fiber-Fat-Fatty-Acids-Cholesterol-Protein-and-Amino-Acids.aspx
    Subtract 10 kcal/d for males and 7 kcal/d for females for each year of age above 19 years.
    """
    age = userprofile.age
    category = userprofile.target.category
    if age > 19.0:
        if category == 'Males':
            age_factor = 10.0 # KCal/day adjustment for each year above age 19
        else:
            age_factor = 7.0
        return val - (age - 19.0)*age_factor
    return val


def get_target_values(userprofile):
    # Retrieve correct target model
    nutrients = userprofile.target.nutrients_set.all()[0]
    target_nutr = {}
    for f in dri_nutrients.keys():
        val = getattr(nutrients, f, None)
        if val is not None:
            if f == 'energy':
                val = adjust_energy(val, userprofile)
            target_nutr[f] = val
    return target_nutr


def model_dict(m, field_names):
    j = {}
    for f in field_names:
        j[f] = unicode(getattr(m, f))
    j['pk'] = m.pk
    return j


class RecipeList(ListView):
    template_name = 'recipe_list.html'  # By default django prepends the app name
    context_object_name = 'recipe_list'
    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user).order_by('-updated')


def delete_recipe(request, pk):
    r = get_object_or_404(Recipe, pk=pk)
    if r.user == request.user:
        r.delete()
    return HttpResponse('Recipe deleted successfully!')


def recipe_page(request, pk=None):
    return render(request, 'recipe2.html', {'recipe_id': pk, })  # empty page, to be filled with data later via AJAX


def get_recipe(request, pk):
    r = get_object_or_404(Recipe, pk=pk)

    # Private?
    if r.private and not r.user == request.user:
        raise Http404('The user who created this recipe flagged it as Private.')

    ingredients = []
    for i in r.ingredient_set.order_by('pk'):
        if i.weight is None:
            if i.unit == 'gram':
                weight = -1
            elif i.unit == 'ounce':
                weight = -2
            else:
                raise Http404('Unit of measure not supported (internal error).')
        else:
            weight = i.weight.pk

        ingredients.append({
            'weight': weight,
            'unit': i.unit,
            'description': i.sr17.Long_Desc,
            'sr17': i.sr17.pk,
            'quantity': i.quantity,
        })

    return JsonResponse({
        'recipe': model_dict(r, RECIPE_FIELDS),
        'ingredients': ingredients,
    })


@login_required
def save_recipe(request, pk=None):
    class RecipeForm(forms.ModelForm):
        class Meta:
            model = Recipe
            fields = RECIPE_FIELDS
    if pk:
        f = RecipeForm(request.POST, instance=get_object_or_404(Recipe, pk=pk))
    else:
        f = RecipeForm(request.POST)
    if f.is_valid():
        # If the recipe was created by another user, this will still work - we save the recipe to this current user's account
        f.instance.user = request.user
        r = f.save()

        # Handle ingredients
        r.ingredient_set.all().delete()  # Clear out all previous ingredients
        for i in json.loads(request.POST['ingredients']):
            if i['weight_id'] in ('-1', '-2'):   # Fake PKs for gram and ounce, respectively
                i.pop('weight_id', None)
            i['recipe'] = r
            model = Ingredient(**i)
            model.save()

        return JsonResponse({ 'pk': r.pk })
    return JsonResponse({ 'errors': f.errors })


def get_nutrition(request):

    # Set up dict of all nutrients listed in database
    nutrients = {}
    for n in NUTR_DEF.objects.all():  # Get complete list of nutrients
        field_name = nut_def_pk2fields[n.pk]['field_name']
        nutrients[field_name]= {
            'name': nut_def_pk2fields[n.pk]['human_name'],
            'value': None,
            'unit': n.Units,
        }

    ingredients = json.loads(request.POST["ingredients_list"])
    for i in ingredients:
        sr17 = get_object_or_404(FOOD_DES, pk=i['sr17'])

        # Conversion to grams is easy - either the ingredient is already in grams or ounces, or
        # we have an entry in the WEIGHT table to handle the conversion.
        w = int(i['weight'])
        if w > 0:
            w = get_object_or_404(WEIGHT, pk=w)
            # Sanity check - WEIGHT record should be linked to the same sr27 FOOD_DES record as the ingredient is!
            if w.NDB_No.pk != sr17.pk:
                raise ValueError
            conv_to_grams = w.Gm_Wgt / w.Amount
        elif w == -2:     # Ounces
            conv_to_grams = 28.349523
        elif w == -1:
            conv_to_grams = 1.0
        else:
            raise ValueError

        # Refuse in SR27 is expressed as a percentage of waste
        q = float(i['quantity'])
        if REFUSE_COMPENSATION:
            q = q * (100.0 - sr17.Refuse)/100.0

        # Compile set of nutrient values
        s = sr17.nutrients_set.all()[0]   # There should be one and only one "Nutrients" model linked to each SR27 FOOD_DES model
        for field_name in nutrients.keys():
            value_per_100g = getattr(s, field_name)
            if value_per_100g is not None:
                ingr_value = q * conv_to_grams * value_per_100g / 100.0
                if nutrients[field_name]['value'] is None:
                    nutrients[field_name]['value'] = ingr_value
                else:
                    nutrients[field_name]['value'] += ingr_value

    if request.user.is_anonymous():
        profile = get_default_userprofile()
    else:
        profile = request.user.userprofile

    return JsonResponse({
        'nutr_data': nutrients,
        'layout': nutrition_display_layout,
        'targets': get_target_values(profile),
    })


def remove_ingredient(request, pk):
    i = get_object_or_404(Ingredient, pk=pk)
    i.delete()
    return JsonResponse({})


def search_ingredient(request):
    s = request.GET['term']
    pks, confidence = parse_food(clean_and_split_search_string(s),True)
    if not pks:
        return JsonResponse([], safe=False)
    foods = FOOD_DES.objects.filter(pk__in=pks[:UI_NUM_FOOD_MATCHES])

    # Scrunch together a list of { pk, description } dicts, in best-match-first order
    d = OrderedDict.fromkeys(pks[:UI_NUM_FOOD_MATCHES])
    for f in foods:
        d[f.pk] = f.Long_Desc

#    return JsonResponse(d.values(), safe=False)
    return JsonResponse([ { 'label': v, 'value': k } for k,v in d.iteritems() ], safe=False)


def get_ingredient_units(request, pk):
    i = get_object_or_404(FOOD_DES, pk=pk)
    units = {}
    for w in i.weight_set.all():
        units[w.pk] = w.Msre_Desc
    # Use fake pk's for ounce and gram if they're not already in the sr27 unit list
    if not 'gram' in units.values():
        units[-1] = 'gram'
    if not 'oz' in units.values() and not 'ounce' in units.values():
        units[-2] = 'ounce'
    return JsonResponse(units)


@login_required
def set_target_category(request):
    category = request.POST.get('category', None)
    age = int( request.POST.get('age', None) )
    if 1 < age and age <= 150:
        t = Target.objects.filter(category=category, age_min__lte=age, age_max__gt=age, type='min')
        if len(t) != 1:
            raise Http404
        profile = request.user.userprofile
        profile.target = t[0]
        profile.age = age
        profile.save()
    else:
        raise Http404
    return JsonResponse([], safe=False)


def get_target_category(request):
    if request.user.is_anonymous():
        profile = get_default_userprofile()
    else:
        profile = request.user.userprofile

    t = profile.target
    tmp = {
        'Males': 'a Male',
        'Females': 'a Female',
        'Pregnancy': 'Pregnancy at',
        'Lactation': 'Breast-Feeding at',
    }
    return JsonResponse({
        'age': profile.age,
        'category': t.category,
        'text': tmp[t.category] + ' age ' + str(profile.age),
    })





not_displayed = (
    'energy_kj',
    'alcohol',
    'water',
    'ash',
    'caffeine',
    'trans_monoenoic_fatty_acids',
    'trans_polyenoic_fatty_acids',
    (
        'amino acids (non-essential)', (
            'alanine',
            'aspartic_acid',
            'glutamic_acid',
        ),
    ),
    # vitamin components
    'retinol',
    'vitamin_a_rae',
    'vitamin_d2',
    'vitamin_d3',
    'vitamin_d2_d3',
    'folic_acid',       # B9 synthetic
    'folate_food',
    'folate_dfe',
    'vitamin_e_added',
    'vitamin_b12_added',

    # phytosterols

    # unsorted
    'adjusted_protein',
    'theobromine',
    'tocotrienol_alpha',
    'tocotrienol_beta',
    'tocotrienol_gamma',
    'tocotrienol_delta',
    'menaquinone_4',
    'dihydrophylloquinone',
    'betaine',
    'hydroxyproline',

        'Amino Acids (conditional)', (
            'arginine',
            'cystine',
            'glycine',
            'proline',
            'serine',
            'tyrosine',
        ),

    # http://www.webmd.com/diet/phytonutrients-faq
    'Phytonutrients', (
        'carotene_beta',
        'carotene_alpha',
        'cryptoxanthin_beta',
        'lutein_zeaxanthin',
        'lycopene',
        'tocopherol_beta',
        'tocopherol_gamma',
        'tocopherol_delta',
        'phytosterols', (
            'stigmasterol',
            'campesterol',
            'beta_sitosterol',
        )
    )

)

nutrition_display_layout__ = (
    'energy',
    'protein', (
        'Amino Acids (essential)', (
            'histidine',
            'isoleucine',
            'leucine',
            'lysine',
            'methionine',
            'phenylalanine',
            'threonine',
            'tryptophan',
            'valine',
        ),
    ),
    'carbohydrate', (
        'fiber',
        'starch',
        'sugars_total', (
            'sucrose',
            'glucose',
            'fructose',
            'lactose',
            'maltose',
            'galactose',
        ),
    ),
    'fat', (
        'monounsaturated_fatty_acids',
        'polyunsaturated_fatty_acids',
        'saturated_fatty_acids',
        'trans_fatty_acids',
    ),
    'cholesterol',
    'Vitamins', (
        'vitamin_a_rae',    # Retinol Activity Equivalent, see comments in dri.py module.
        'thiamin',          # B1
        'riboflavin',       # B2
        'niacin',           # B3
        'pantothenic_acid', # B5
        'vitamin_b6',       # B6
                            # B7 (Biotin)???
        'folate',           # B9
        'vitamin_b12',      # B12
        'vitamin_c',
        'vitamin_d',
        'vitamin_e',
        'vitamin_k',
        # Additional
        'choline',

    ),
    'Minerals', (
        'calcium',
        'copper',
        'iron',
        'fluoride',
        'magnesium',
        'manganese',
        'phosphorus',
        'potassium',
        'selenium',
        'sodium',
        'zinc',
    ),
)
