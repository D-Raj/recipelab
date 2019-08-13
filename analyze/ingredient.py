# -*- coding: utf-8 -*-

from django.db.models import Q
from django.utils.translation import ugettext as _

from sr17.models import FOOD_DES, WEIGHT
import string
import re
import pdb

FOOD_MATCH_WORD_MIN_CHARS = 1
BRAND_NAME_MIN_CHARS = 2    # minimum length to use when deciding to reject entries that have brand names
FAKE_WEIGHT_PK_ASSUME_DENSITY = -2
FAKE_WEIGHT_PK_GRAMS = -1

DEBUG = False
RANKING_DEBUG = False

# from inflection import pluralize, singularize   # For pluralization
import inflect  # Use this lib instead because we can easily add exceptions/rules
p = inflect.engine()
p.defnoun( "slice", "slice" ) # The singular of slice is slice, not slouse...
p_cache = {}
def singularize(s):
    sing = p.singular_noun(s)
    if sing:
        return sing
    return s

    attempt = p_cache.get(s, None)
    if attempt:
        return attempt
    sing = p.singular_noun(s)
    p_cache[s] = sing
    if sing:
        return sing
    return s

# These can be safely ignored while trying to match ingredient to FOOD_DES.Long_Des
quantity_only_words = (
    "bag",
    "bar",
    "bird",
    "bird",
    "block",
    "bottle",
    "bowl",
    "box ",
    "bucket",
    "bunch",
    "bushel",
    "can",
    "centiliter",
    "centilitre",
    "cl",
    "container",
    "cube",
    "cubic",
    "centimeter",
    "inch",
    "cup",
    "dash",
    "deciliter",
    "decilitre",
    "dl",
    "dram",
    "drop",
    "each",
    "floret",
    "fl",
    "oz",
    "dram",
    "ounce",
    "g",
    "gallon",
    "gram",
    "half",
    "halves",
    "inch",
    "individual",
    "item",
    "jar",
    "jumbo",
    "kg",
    "kilogram",
    "l",
    "large",
    "lb",
    "lb",
    "link",
    "liter",
    "litre",
    "loaf",
    "measure",
    "milliliter",
    "millilitre",
    "mini",
    "ml",
    "order",
    "ounce",
    "ounce",
    "oz",
    "pack",
    "package",
    "packet",
    "pat",
    "pattie",
    "patty",
    "piece",
    "pinch",
    "pint",
    "pint",
    "portion",
    "pouch",
    "pound",
    "quart",
    "recipe",
    "yield",
    "scoop",
    "serving",
    "set",
    "sheet",
    "slice",
    "small",
    "spoon",
    "sprig",
    "square",
    "tablespoon",
    "tbsp",
    "tbs",
    "teaspoon",
    "tsp",
    "unit",                  
)

# Ref: http://www.onlineconversion.com/
#     Minimum 6 significant digits accuracy
table_conv_to_litres = {
    'cl': 0.01,
    'centiliter': 0.01,
    'centilitre': 0.01,
    'l': 1.0,
    'liter': 1.0,
    'litre': 1.0,
    'ml': 0.001,
    'milliliter': 0.001,
    'millilitre': 0.001,
    'cc': 0.001,
    'cubic cm': 0.001,
    'cubic centimeter': 0.001,
    'cubic centimetre': 0.001,
    'cm3': 0.001,
    'cup': 0.25,
    'us cup': 0.2365882365,
    'canada cup': 0.2273045,
    'fifth': 0.7570823568,
    'gallon': 3.785411784,
    'us gallon': 3.785411784,
    'uk gallon': 4.54609,
    'imperial gallon': 4.54609,
    'fl oz': 0.029573529563,
    'fl ounce': 0.029573529563,
    'fluid ounce': 0.029573529563,
    'liquid oz': 0.029573529563,
    'liquid ounce': 0.029573529563,
    'us fl oz': 0.029573529563,
    'us fl ounce': 0.029573529563,
    'us fluid ounce': 0.029573529563,
    'uk fl oz': 0.0284130625,
    'uk fl ounce': 0.0284130625,
    'uk fluid ounce': 0.0284130625,
    'pint': 0.473176473,
    'us pint': 0.473176473,
    'uk pint':  0.56826125,
    'quart': 0.946352946,
    'us quart': 0.946352946,
    'uk quart': 1.1365225,
    'tablespoon': 0.015,
    'tbsp': 0.015,
    'tbs': 0.015,
    'metric tablespoon': 0.015,
    'metric tbsp': 0.015,
    'metric tbs': 0.015,
    'us tbsp': 0.014786764781,
    'us tbs': 0.014786764781,
    'us tablespoon': 0.014786764781,
    'uk tbsp': 0.01420653125,
    'uk tbs': 0.01420653125,
    'uk tablespoon': 0.01420653125,
    'teaspoon': 0.005,
    'tsp': 0.005,
    'metric teaspoon': 0.005,
    'metric tsp': 0.005,
    'us tsp': 0.0049289215938,
    'us teaspoon': 0.0049289215938,
    'uk tsp': 0.0035516328125,
    'uk teaspoon': 0.0035516328125,
    'dash': 0.00061611519922,    # 1/8 of US teaspoon
    'drop': 0.000051342933268, 
    'pinch': 0.00030805759961,
}

table_conv_to_grams = {
    'g': 1.0,
    'gram': 1.0,
    'cg': 0.01,
    'centigram': 0.01,
    'dg': 0.1,
    'decigram': 0.1,
    'kg': 1000.0,
    'kilogram': 1000.0,
    'mg': 0.001,
    'milligram': 0.001,
    'lb': 453.59237,
    'pound': 453.59237,
    'oz': 28.349523125,
    'ounce': 28.34952312,
    'butter stick': 113.3980925,
}

number_unicode_fractions = {
    '½': 0.5,
    '⅓': 0.333333333,
    '⅔': 0.666666666,
    '¼': 0.25,
    '¾': 0.75,
    '⅕': 0.2,
    '⅖': 0.4,
    '⅗': 0.6,
    '⅘': 0.8,
    '⅙': 0.166666666,
    '⅚': 0.833333333,
    '⅛': 0.125,
    '⅜': 0.375,
    '⅝': 0.625,
    '⅞': 0.875,
}

number_terms = {
    'half': 0.5,
    'third': 0.333333333,
    'quarter': 0.25,
    'fifth': 0.20,    # This can be a unit of volume as well!  More likely to be used as a number word
    'sixth': 0.166666666,
    'seventh': 0.142857142,
    'eighth': 0.125,
    'ninth': 0.1111111111,
    'tenth': 0.1,
#
    'dozen': 12.0,
#
    'one': 1.0,
    'two': 2.0,
    'three': 3.0,
    'four': 4.0,
    'five': 5.0,
    'six': 6.0,
    'seven': 7.0,
    'eight': 8.0,
    'nine': 9.0,
    'ten': 10.0,
    'eleven': 11.0,
    'twelve': 12.0,
    'thirteen': 13.0,
    'fourteen': 14.0,
    'fifteen': 15.0,
    'sixteen': 16.0,
    'seventeen': 17.0,
    'eighteen': 18.0,
    'nineteen': 19.0,
    'twenty': 20.0,
}

# TODO: Use this in decode function
pre_parsing_word_substitutions = {
    'T': 'tablespoon',
    't': 'teaspoon',
}

# TODO: Use this in decode function and also run sr17 description through this substitution, making sure to adjust for any double-space errors (strip and join)
pre_parsing_letter_substitutions = {
    '%': ' percent '
}

uncooked_ingredient_words = (
    'raw',
    'spices',
    'whole',
    'fresh',
)

single_serving_words = (
    'serving',
    'slice',
    'bird',
    'pat',
    'can',
    'package',
    'piece',
    'bar',
    'pod',
    'item',
    'container',
    'steak',
    'fruit',
)

def food_word_aliases(s):
    """
    Returns a list of aliases for s.
    """
    a = (
        ('low','reduced'),
        ('low fat','low-fat','lowfat'),
        ('no fat','no-fat','nofat'),
        ('unsalted', 'without salt', 'no salt'),  # useless at this point because match algorithm uses whole words only
        ('salted', 'with salt', 'salt added'),    # also useless
    )
    for b in a:
        if s in b:
            return [ w for w in b if not w==s ]  # return all the other words from the list
    return []



def contains_brand(s):
    # In SR-17, brands are the only all-capital words
    words = s.split()
    for word in words:
        w = ''.join(c for c in word if c.isalpha())  # Get rid of non-alphabetical chars, especially commas and apostrophes!
        if len(w) > BRAND_NAME_MIN_CHARS and sum(1 for c in w if c.isupper()) == len(w):
            return True
    return False


def parse_food(s_words, show_branded_products=True):
    """
    Grab any entry in FOOD_DES that contains any of the words, then rank them and return a sorted listed (best match first)
    """

    # Ignore single-letter words and quantity terms
    words = [ w for w in s_words if len(w) > FOOD_MATCH_WORD_MIN_CHARS and not w in quantity_only_words ]

    if len(words) == 0:
        return [], 0.0

    query = Q(Long_Desc__icontains=words[0])
    for w in words[1:]:
        query = query | Q(Long_Desc__icontains=w)
    entries = FOOD_DES.objects.filter(query)

    # matches has the form
    # {  
    #     "10421":
    #     {
    #         "low": 3,
    #         "fat": 3,
    #         "milk": 0,
    #     }
    # }
    matches = {}

    # ranking has the form, where the integer measures quality of match
    # {
    #     "10421": 201,
    #     "10522": 189,
    # }
    ranking = {}
    best_num_word_matches = 0
    for e in entries:

        if not show_branded_products and contains_brand(e.Long_Desc):
            continue
        
        this_entry_num_word_matches = 0
        l = e.Long_Desc.lower()
        # Each commasep is a list of words
        commasep_wordlists = [ clean_and_split_search_string(term) for term in l.split(',') ]

        # Ranking boost if sr17 entry has uncooked_ingredient_words
        # Get big boost for matching single word, and an incremental increase for additional words
        uncooked_ingredient = 0.0
        matching = [ u for u in sum(commasep_wordlists, []) if u in uncooked_ingredient_words ] # Use sum() to flatten the list of lists
        if matching:
            uncooked_ingredient = 1.0 + float(len(matching)) / 5.0
        
        # Check if we have a BINGO! match - one of the comma-separated word lists is entirely contained in the search string
        # Left-hand comma-separated terms are much more important than right-hand terms
        commasep_list_total_match = 0.0
        for i, commasep_wordlist in enumerate(commasep_wordlists):
            matching = [ a for a in commasep_wordlist if a in words ]
            if len(matching) == len(commasep_wordlist):
                # Linear decay of ranking importance as we go from left to right along the comma-separated terms
                # rank_boost will be 1.0 if left-most term is matching, and will decay toward 0.0 as you work your way to the right
                rank_boost = (float(len(commasep_wordlists)) - i) / float(len(commasep_wordlists))
                commasep_list_total_match += rank_boost

        # For each comma separated string in FOOD_DES.Long_Desc field, try to match each search word
        # A comma_word_position is the position in the comma-separated list of description in FOOD_DES:
        #    Butter, whipped, with salt
        #    0,1,2
        matches[e.pk] = {}
        sum_of_comma_word_positions = 0
        for i, commasep_wordlist in enumerate(commasep_wordlists):
            for w in words:
                if w in commasep_wordlist:    #  Matches whole words
                    # Record the match (so you can easily see how many terms are matched)
                    matches[e.pk][w] = i
                    # Matching a term at the left end of the food description is more valuable, so use the "comma position" to handicap the ranking
                    sum_of_comma_word_positions += i
                else:
                    # Look up all known aliases of the search word  TODO: This doesn't handle multi-word aliases at all!
                    for a in food_word_aliases(w):
                        if a in commasep_wordlist:
                            # Record the match (so you can easily see how many terms are matched)
                            matches[e.pk][w] = i
                            # Matching a term at the left end of the food description is more valuable, so use the "comma position" to handicap the ranking
                            sum_of_comma_word_positions += i
                            break

        k_num_matches = 100.0
        k_comma_positions = -10.0
        k_desc_length = -1.0
        k_commasep_list_total_match = 50.0
        k_uncooked_ingredient = 25.0
        
        ranking[e.pk] = ( len(matches[e.pk]) * k_num_matches ) \
            + sum_of_comma_word_positions * k_comma_positions \
            + len(unicode(e.Long_Desc)) * k_desc_length \
            + commasep_list_total_match * k_commasep_list_total_match \
            + uncooked_ingredient * k_uncooked_ingredient

        if RANKING_DEBUG:
            print '-----------------------------------------------------------'
            print l
            print 'Rank: ' + str( ranking[e.pk] )
            print '    ' + str(len(matches[e.pk]) * k_num_matches)  + ' Num matches: ' + str(len(matches[e.pk])) + ' k: ' + str(k_num_matches)
            print '    ' + str(sum_of_comma_word_positions * k_comma_positions) + ' Comma word-positions: ' + str(sum_of_comma_word_positions) + ' k: ' + str(k_comma_positions)
            print '    ' + str(len(unicode(e.Long_Desc)) * k_desc_length) + ' Length: ' + str(len(unicode(e.Long_Desc))) + ' k: ' + str(k_desc_length)
            print '    ' + str(commasep_list_total_match * k_commasep_list_total_match) + ' Comma-sep bingo match: ' + str(commasep_list_total_match) + ' k: ' + str(k_commasep_list_total_match)
            print '    ' + str(uncooked_ingredient * k_uncooked_ingredient) + ' Uncooked words: ' + str(uncooked_ingredient) + ' k: ' + str(k_uncooked_ingredient)


    # No word was matched
    if not ranking:
        return None, 0.0

    pks = sorted(ranking, key=ranking.get, reverse=True)
    confidence = float( len(matches[pks[0]]) ) / float(len(words))
    
    if DEBUG:
        for pk in pks[:10]:
            food = FOOD_DES.objects.get(pk=pk)
            print unicode(food) + '  [ranking:' + str(ranking[pk]) + ']'
            weights = food.weight_set.all()
            for w in weights:
                print '    ' + w.Msre_Desc
    if DEBUG:
        print '-----------------------------------------------------------'
        print 'best_num_word_matches = ' + str(best_num_word_matches)
        print 'len(words) = ' + str(len(words))
        print 'Confidence = ' + str(confidence)

    return pks, confidence  #  A list of PKs (FOOD_DES.NDB.No) sorted by best match


def parse_numbers_pure_number(words):
    """
    Try to find a first pure number (e.g. '3', '4.32').
    Returns the number if found, and the rest of the string.
    """
    words_before_num = words
    words_after_num = []
    n1 = None
    for i in range(len(words)):
        try:
            n1 = float(words[i])
            if n1 <= 0.0:
                n1 = None
                raise ValueError(_("Can't make sense of Negative or Zero quantity"))
            words.pop(i)
            words_before_num = words[:i]
            words_after_num = words[i:]
            break
        except ValueError:
            continue
    return words_before_num, n1, words_after_num


def parse_numbers_fraction(words):
    """
    Try to find a fraction (e.g. '1/5', '4.3/3.2', '⅚').  
    Also handles a number before a fraction, whether it's stuck on or space delimited (e.g. '1⅚', '3 3/4')
    Returns the number if found, and the rest of the string.
    """
    search_for_number_in_front_of_fraction = True
    words_before_num = words
    words_after_num = []
    n1 = None
    for i in range(len(words)):
        m1 = re.match(r'^([0-9.]+)/([0-9.]+)$', words[i])
        pattern = r'^([0-9])*([' + ''.join(number_unicode_fractions.keys()) + r']+)$' # This won't work without the '+', which means it will match repeated chars!
        m2 = re.match(pattern, words[i])
#        m2 = re.match(r'^([0-9])*([½⅓⅔¼¾⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞]+)$', words[i]) 
        
        # Fractions of the form a/b
        if m1:
            try:
                n1 = float(m1.group(1)) / float(m1.group(2))
            except:
                continue
        # Unicode fractions with optional leading number e.g. '⅓', '5⅓'
        elif m2 and m2.group(2) in number_unicode_fractions.keys(): # Hack for avoiding repeated fraction characters - reject anything not recognized
            n1 = m2.group(1)
            n2 = m2.group(2) 
            if not n1 is None:
                n1 = float(n1)
                search_for_number_in_front_of_fraction = False  # No need to search for space-delimited number in front of fraction, we've found one stuck on 
            else:
                n1 = 0.0
            n2 = number_unicode_fractions[n2]
            n1 = n1 + n2
        else:
            continue
        words.pop(i)  # Remove fraction (and leading number)
        idx = i

        # Look for space-limited number before fraction (e.g. the 2 in '2 1/2)' - we've already split the space-limited string into words
        if i >= 1 and re.match('^[0-9.]+$', words[i-1]) and search_for_number_in_front_of_fraction:
            try:
                n1 += float(words[i-1])
                words.pop(i-1) # Remove number before fraction
                idx = i - 1
            except:
                pass
            
        words_before_num = words[:idx]
        words_after_num = words[idx:]
        break
            
    return words_before_num, n1, words_after_num


def parse_numbers_second_number_term(words_after_num):
    """
    Call this function if a first number was found.  In that case, we search the remaining part of the string (to the right of the found number)
    to see it begins with a number_term.  This deals with cases like '1/2 dozen' and 'three fifths'
    """
    n2 = None
    for term in number_terms.keys():
        term_words = term.split()
        if words_after_num[:len(term_words)] == term_words:
            n2 = number_terms[term]
            for j in range(len(term_words)):
                words_after_num.pop(0)    # Remove the number term words
    return n2, words_after_num


def parse_numbers_term(words):
    """
    Try to find a "number term" (like "twenty")
    If the "number term" has multiple words, they must occur consecutively
    We prioritize the words near the beginning of s_clean by starting the search from that end.
    Returns the number if found, and the rest of the string.
    """
    words_before_num = words
    words_after_num = []
    n1 = None
    for i in range(len(words)):
        keys = number_terms.keys()
        keys.sort(key=lambda t: len(t), reverse=True) # Match the longest number terms first, so we hit 'twenty one' before 'twenty'
        for term in keys:
            term_words = term.split()
            if words[i:i+len(term_words)] == term_words:
                n1 = number_terms[term]
                for j in range(len(term_words)):
                    words.pop(i)    # Remove the number term words
                words_before_num = words[:i]
                words_after_num = words[i:]
            if not n1 is None:
                break
    return words_before_num, n1, words_after_num
            

def parse_numbers(words):
    """
    Find quantity number in words which is assumed to be stripped of leading/trailing space, illegal characters and multi-spaces.
    """
    words_before_num = words
    n1 = None

    # idx is the index of the first word
    if n1 is None:
        words_before_num, n1, words_after_num = parse_numbers_pure_number(words_before_num)
    if n1 is None:
        words_before_num, n1, words_after_num = parse_numbers_fraction(words_before_num)
    if n1 is None:
        words_before_num, n1, words_after_num = parse_numbers_term(words_before_num)
    if n1 is None:
        return words, 1.0  # Default quantity, and unmodified words
    
    # Search for a second number occurring just after the first (e.g. '2 dozen', 'three fifths').  Must be a number_term (using words)
    n2, words_after_both_numbers = parse_numbers_second_number_term(words_after_num)
    if not n2 is None:
        n1 *= n2
        return words_before_num + words_after_both_numbers, n1

    return words_before_num + words_after_num, n1



def parse_units_by_conv_factor_list(words, conv_factor_list):
    words_before_unit = []
    found_unit = None
    words_after_unit = []
    conv_factor = None
    keys = conv_factor_list.keys()
    keys.sort(key=lambda t: len(t), reverse=True) # Match the longest unit entries first, so we hit 'us fl oz' before 'fl oz'
    for unit in keys:
        found_idx = {}
        try:
            unit_words = unit.split()
            for unit_word in unit.split():
                found_idx[unit_word] = words.index(unit_word)
            # Made it this far, all the unit's words were found
            # Ensure they are consecutive
            t = found_idx.values()
            t.sort()
            o = t[0]
            for i, idx in enumerate(t):
                if not idx == i+o:
                    break
            else:
                # All found words are consecutive, we fell off the end of the loop with no break
                found_unit = unit
                conv_factor = conv_factor_list[unit]
                words_before_unit = words[:o]
                words_after_unit = words[o+len(unit_words):]
                break

        except ValueError:
            pass
    return words_before_unit, found_unit, words_after_unit, conv_factor


def parse_units(words):
    # Volume-based units - each unit may have multiple words, which can be used in any order but must be consecutive
    words_before_unit, unit, words_after_unit, ingr_conv_to_litres = parse_units_by_conv_factor_list(words, table_conv_to_litres)
    if not ingr_conv_to_litres is None:
        return words_before_unit, unit, words_after_unit, ingr_conv_to_litres, None  # return None as the mass conversion factor
        
    words_before_unit, unit, words_after_unit, ingr_conv_to_grams = parse_units_by_conv_factor_list(words, table_conv_to_grams)
    if not ingr_conv_to_grams is None:
        return words_before_unit, unit, words_after_unit, None, ingr_conv_to_grams  # return None as the volume conversion factor

    return words, None, [], None, None   # No unit found, assume it's 'piece' and return no conversion factor
    

def clean_and_split_search_string(s):
    # Remove illegal characters
    s_clean = ''.join(c for c in s if c in string.ascii_letters + ' 0123456789%-/')

    # Run a few subtitutions before changing all chars to lower-case, so we can catch 'T' for tablespoon and 't' for teaspoon
    words = s_clean.strip().split() # This step also deals with multi-spaces
    for i, w in enumerate(words):
        if w in pre_parsing_word_substitutions.keys():
            words[i] = pre_parsing_word_substitutions[w]

    # lower-case only!
    words = [ w.lower() for w in words ]

    # Use singular words only for all processing
    words = [ singularize(w) for w in words ]

    return words


def get_ingr_conv_to_grams(sr17_food_pk, words):
    """
    For a given sr17 FOOD_DES entry, and values already parsed from the INGRedient string,
    return a total conversion factor from ingredient quantity units to grams.
        ingr_grams = ingr_quantity_number * total_conversion
        
    TODO: Should we be calculating a conversion factor for each WEIGHT entry, ranking them and choosing the best one?
          By doing it that way, we can split off a function that returns the conversion factor for any given WEIGHT
          entry, which will be useful if the user is allowed to select the WEIGHT entry from a drop-down list...
    """

    ##################################################################################
    # Try to find a Mass unit - that's the easy way!
    ##################################################################################
    #
    w_before, unit, w_after, ingr_conv_to_grams = parse_units_by_conv_factor_list(words, table_conv_to_grams)
    if not ingr_conv_to_grams is None:
        return unit, ingr_conv_to_grams, 'Ingredient given in mass units, no need to convert', 1.0


    ##################################################################################
    # Try to find a Volume unit
    ##################################################################################
    #
    # First, get the entries in the sr17 WEIGHT table (unit equivalence table) for this sr17 FOOD_DES food item
    f = FOOD_DES.objects.get(pk=sr17_food_pk)
    WEIGHTS = f.weight_set.all()
    w_before, unit, w_after, ingr_conv_to_litres = parse_units_by_conv_factor_list(words, table_conv_to_litres)

    # If the ingredient was given in terms of volume, we find the best match from the SR17 volume equivalences
    if not ingr_conv_to_litres is None:
        # Rank them according to how many non-unit words they match in our ingredient string
        ranking = {}
        conv_values = {}
        for w in WEIGHTS:
            # Try to convert this WEIGHT entry to litres
            W_before, sr17_unit, W_after, sr17_conv_to_litres = parse_units_by_conv_factor_list(clean_and_split_search_string(w.Msre_Desc), table_conv_to_litres)
            # If this WEIGHT entry is indeed in volume units, try to match any other terms from the WEIGHT table description to our ingredient string (e.g. shredded)
            if not sr17_unit is None:

                # To use WEIGHT entry values for converting our ingredient to '100 g'
                #     WEIGHT table has entries like
                #         Amount | Msre_Desc | Gm_Wgt
                #         -------+-----------+-------
                #         5.0    | fl oz     | 60.0
                #
                #     This means that if you can take a quantity number A in fl oz and get the gram weight as follows:
                #         Grams = A * 60.0/5.0
                #     If you had a quantity B in litres, you would first convert it to fl oz:
                #         Grams = (B/conv_to_litres['fl oz']) * 60.0/5.0
                #     So the general conversion from litres to Grams is:
                #         Grams = (1/conv_to_litres[Msre_Desc_unit]) * Gm_Wgt/Amount
                #     But our ingredient quantity must also be converted to litres first.  We already know that conversion factor, so:
                #         Grams = ingredient_quantity * ingr_conv_to_litres * (1/conv_to_litres[Msre_Desc_unit]) * Gm_Wgt/Amount
                #
                conv_values[w.pk] = {
                    'unit':unit,
                    'ingr_conv_to_grams': ingr_conv_to_litres * (1.0/sr17_conv_to_litres) * w.Gm_Wgt/w.Amount
                } # Store these

                ranking[w.pk] = 0
                for word in W_before + W_after:
                    if word in w_before + w_after:
                        ranking[w.pk] += 1
        sorted_ranking = sorted(ranking, key=ranking.get, reverse=True) # If no non-unit words were matched, ranking is all-zero and this will produce random order...
        if sorted_ranking:
            cv = conv_values[sorted_ranking[0]]
            return cv['unit'], cv['ingr_conv_to_grams'], 'Ingredient volume unit ' + unit + ' converted to WEIGHT table unit ' + cv['unit'], 0.8
            
        # If no volume equivalent was given in sr17, but our ingredient was given in terms of volume, assume density of water and issue warning
        assumed_density_g_per_l = 1000.0
        return unit, ingr_conv_to_litres * assumed_density_g_per_l, 'Ingredient volume unit is ' + unit + '. Could not find any volume in WEIGHT table, so we assumed density=Water and used grams.', 0.4

    ##################################################################################
    # Try to find a 'pieces' type unit (cans, slices, birds, etc.)
    ##################################################################################
    #
    # Find best match in WEIGHT desc, the one that more likely resembles a 'pieces' unit
    ranking = {}
    conv_values = {}
    for w in WEIGHTS:
        ranking[w.pk] = 0

        # Use the parsing function to strip the WEIGHT entry description of unit-related words
        w0_before, vol_unit, w0_after, tmp = parse_units_by_conv_factor_list(clean_and_split_search_string(w.Msre_Desc), table_conv_to_litres)
        w1_before, mass_unit, w1_after, tmp = parse_units_by_conv_factor_list(' '.join(w0_before + w0_after), table_conv_to_grams)
        non_unit_words = w1_before + w1_after

        conv_values[w.pk] = { 'unit':w.Msre_Desc, 'Gm_Wgt':w.Gm_Wgt, 'Amount':w.Amount } # Store these
        # Try to match non-unit terms from the WEIGHT table description to our ingredient string (e.g. slice)
        for w in non_unit_words:
            if w in words:
                ranking[w.pk] += 5
        # Try to find words suggesting a single serving, in the WEIGHT entry
        for w in non_unit_words:
            if w in single_serving_words:
                ranking[w.pk] += 1
        # WEIGHT entries with no units in them are more likely a match for a unitless ingredient
        if vol_unit is None and mass_unit is None:
                ranking[w.pk] += 3
                
    ranked_pks = sorted(ranking, key=ranking.get, reverse=True) # If no non-unit words were matched, ranking is all-zero and this will produce random order...
    cv = conv_values[ranked_pks[0]]
    ingr_conv_to_grams = cv['Gm_Wgt']/cv['Amount']
    return cv['unit'], ingr_conv_to_grams, 'Ingredient was unit-less, the best match in WEIGHT table is ' + cv['unit'], 0.6


def decode(s):
    quantity = None
    unit = None
    best_food_match = None
    conv_to_grams = None
    confidence_food = None
    confidence_unit = None
    sr17_food_pks = []
    msg = None

    words = clean_and_split_search_string(s)
    
    # Extract quantity number from s
    words_numberless, quantity = parse_numbers(words)

    # pks for each entry in FOOD_DES that matched at least one word from the search string, sorted in order of descending relevance
    sr17_food_pks, confidence_food = parse_food(words_numberless)

    # Remember, it's entirely possible there was no matching food item at all
    if sr17_food_pks:
        # weight_pk refers to an entry in the WEIGHT table (linked to SR17's FOOD_DES table)
        unit, conv_to_grams, msg, confidence_unit = get_ingr_conv_to_grams(sr17_food_pks[0], words_numberless)
        # Massage the output
        best_food_match = FOOD_DES.objects.get(pk=sr17_food_pks[0])

    if DEBUG:
        print 'Quantity:' + str(quantity) + ', Unit:' + str(unit) + \
            ', Conversion to grams:' + str(conv_to_grams) + \
            ', msg:' + str(msg)

    return {
        'quantity': quantity,
        'unit': unit,
        'sr17': best_food_match,
        'conv_to_grams': conv_to_grams,
        'confidence_food': confidence_food,
        'confidence_unit': confidence_unit,
        'sr17_match_pks': sr17_food_pks,
    }
