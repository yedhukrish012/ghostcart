from django.shortcuts import get_object_or_404, render
from .models import category, product

# Create your views here.
def store(request,category_slug = None):
    categories = None
    products   = None
    
    if category_slug != None:
        categories = get_object_or_404(category, slug =  category_slug)
        products = product.objects.filter(category = categories,is_available = True)
        product_count = products.count()

    else:
        products = product.objects.all().filter(is_available = True)
        product_count = products.count()

    context = {
        "products" : products,
        "product_count" : product_count
    }
    return render(request,'store/store1.html',context)