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


def product_details(requst, category_slug, product_slug):
    try:
        single_product = product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    context = {
        'single_product' : single_product
    }
    return render(requst,'store/product_details.html',context)