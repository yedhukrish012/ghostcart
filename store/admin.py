from django.contrib import admin
from store.models import ProductImage, ReviewRating, Wishlist, category, product,Variation

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug':('category_name',)}

class PictureInline(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines = [PictureInline]

admin.site.register(product, ProductAdmin)

admin.site.register(category,CategoryAdmin)

admin.site.register(Variation)

admin.site.register(ReviewRating)

admin.site.register(Wishlist)


