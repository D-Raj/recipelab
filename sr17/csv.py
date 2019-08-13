import codecs
from models import *
#from csvImporter.model import CsvDbModel
from adaptor.model import CsvDbModel

DIR = "/home/djr/recipelab/work/"

# Notes:
#     data = [ line.replace('~','') for line in open("/home/djr/recipelab/work/FD_GROUP.txt") ]
#     t = csv_FD_GROUP.import_data(data)


#######################################################################

class csv_FD_GROUP(CsvDbModel):
    class Meta:
        dbModel = FD_GROUP
        delimiter = "^"

class csv_FOOD_DES(CsvDbModel):
    class Meta:
        dbModel = FOOD_DES
        delimiter = "^"

class csv_LANGDESC(CsvDbModel):
    class Meta:
        dbModel = LANGDESC
        delimiter = "^"

class csv_LANGUAL(CsvDbModel):
    class Meta:
        dbModel = LANGUAL
        delimiter = "^"

class csv_NUTR_DEF(CsvDbModel):
    class Meta:
        dbModel = NUTR_DEF
        delimiter = "^"

class csv_SRC_CD(CsvDbModel):
    class Meta:
        dbModel = SRC_CD
        delimiter = "^"

class csv_DERIV_CD(CsvDbModel):
    class Meta:
        dbModel = DERIV_CD
        delimiter = "^"

class csv_WEIGHT(CsvDbModel):
    class Meta:
        dbModel = WEIGHT
        delimiter = "^"

class csv_FOOTNOTE(CsvDbModel):
    class Meta:
        dbModel = FOOTNOTE
        delimiter = "^"

class csv_NUT_DATA(CsvDbModel):
    class Meta:
        dbModel = NUT_DATA
        delimiter = "^"

class csv_DATA_SRC(CsvDbModel):
    class Meta:
        dbModel = DATA_SRC
        delimiter = "^"

class csv_DATSRCLN(CsvDbModel):
    class Meta:
        dbModel = DATSRCLN
        delimiter = "^"

#######################################################################

def clean_sr17_datafile(fn):
    # need latin-1 due to mu character (U+00b5) in NUTR_DEF.txt
    f = codecs.open(DIR + fn + '.txt', mode='rb', encoding='latin-1') # TODO: use os.path
    print 'Processing ' + fn
    return [ line.replace('~', '') for line in f ] # TODO: use os.path


def import_sr17():
    csv_FD_GROUP.import_data(clean_sr17_datafile('FD_GROUP'))
    csv_FOOD_DES.import_data(clean_sr17_datafile('FOOD_DES'))
    csv_LANGDESC.import_data(clean_sr17_datafile('LANGDESC'))
    csv_LANGUAL.import_data(clean_sr17_datafile('LANGUAL'))
    csv_NUTR_DEF.import_data(clean_sr17_datafile('NUTR_DEF'))
    csv_SRC_CD.import_data(clean_sr17_datafile('SRC_CD'))
    csv_DERIV_CD.import_data(clean_sr17_datafile('DERIV_CD'))
    csv_WEIGHT.import_data(clean_sr17_datafile('WEIGHT'))
    csv_FOOTNOTE.import_data(clean_sr17_datafile('FOOTNOTE'))
    csv_NUT_DATA.import_data(clean_sr17_datafile('NUT_DATA'))
    csv_DATA_SRC.import_data(clean_sr17_datafile('DATA_SRC'))
    csv_DATSRCLN.import_data(clean_sr17_datafile('DATSRCLN'))
    