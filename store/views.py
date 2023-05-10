from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from carts.models import Cartitem
from carts.views import _cart_id
from .models import ProductImage, category, product

# Create your views here.
def store(request,category_slug = None):
    categories = None
    products   = None
    
    if category_slug != None:
        categories = get_object_or_404(category, slug =  category_slug)
        products = product.objects.filter(category = categories,is_available = True)
        paginator = Paginator(products,1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    else:
        products = product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products,2)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        "products" : paged_products,
        "product_count" : product_count
    }
    return render(request,'store/store1.html',context)


def product_details(request, category_slug, product_slug):
    try:
        single_product = product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = Cartitem.objects.filter(cart__cart_id = _cart_id(request),Product=single_product).exists()
        pictures = ProductImage.objects.filter(product=single_product)
        print(pictures)
    except Exception as e:
        raise e
    context = {
        'single_product' : single_product,
        'in_cart' : in_cart,
        'pictures' : pictures 
    }
    return render(request,'store/product_details.html',context)

def search(request):
    return render(request,'store/store1.html')