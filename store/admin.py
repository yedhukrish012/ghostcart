from django.contrib import admin
from store.models import category, product,Variation

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug':('category_name',)}

admin.site.register(category,CategoryAdmin)
admin.site.register(product)
admin.site.register(Variation)


