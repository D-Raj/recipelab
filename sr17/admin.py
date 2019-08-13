from django.contrib import admin
from sr17.models import *

admin.site.register(FOOD_DES)
admin.site.register(FD_GROUP)
admin.site.register(LANGDESC)
admin.site.register(LANGUAL)
admin.site.register(NUTR_DEF)
admin.site.register(SRC_CD)
admin.site.register(DERIV_CD)
admin.site.register(WEIGHT)
admin.site.register(FOOTNOTE)
admin.site.register(NUT_DATA)
admin.site.register(DATA_SRC)
admin.site.register(DATSRCLN)


class NUT_DATA_Inline(admin.TabularInline):
    model = NUT_DATA
    fk_name = "NDB_No"
class FOOD_DES_Admin(admin.ModelAdmin):
    inlines = [
        NUT_DATA_Inline,
    ]    
# admin.site.register(FOOD_DES, FOOD_DES_Admin)
    
