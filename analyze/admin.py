from django.contrib import admin
from analyze.models import *

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(TargetSource)
admin.site.register(Target)
admin.site.register(UserProfile)
admin.site.register(Nutrients)

