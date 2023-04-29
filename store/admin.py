from django.contrib import admin
from store.models import category, product,Variation

# Register your models here.
admin.site.register(category)
admin.site.register(product)
admin.site.register(Variation)


