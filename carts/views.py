from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect, render
from . models import Cart, Cartitem
from store.models import product

# Create your views here.
def mycart(request,total = 0, quantity = 0, cart_items = None):
    try:
        mycart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = Cartitem.objects.filter(cart=mycart,is_active=True)
        for item in cart_items:
            total += (item.Product.price*item.quantity)
            quantity += item.quantity
        tax = (.12 * total)
        grand_total = total + tax    
    except:
        pass
    context = {
        'total':total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total' : grand_total,

               }

    return render(request,'store/carts.html',context)


def _cart_id(request):
    mycart = request.session.session_key
    if not mycart:
        mycart = request.session.create()
    return mycart

def add_cart(request,product_id):
    myproduct = product.objects.get(id=product_id)
    try:
        mycart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        mycart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    mycart.save()

    try:
        cart_item = Cartitem.objects.get(Product=myproduct,cart=mycart)
        cart_item.quantity += 1
        cart_item.save()
    except Cartitem.DoesNotExist:
        cart_item = Cartitem.objects.create(
            Product = myproduct,
            quantity = 1,
            cart = mycart,
        )
        cart_item.save()
    return redirect('mycart')

def remove_cart(request,product_id):
    mycart = Cart.objects.get(cart_id=_cart_id(request))
    myproduct = get_object_or_404(product,id=product_id)
    cart_item = Cartitem.objects.get(Product=myproduct,cart=mycart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('mycart')

def del_cart(request,product_id):
    cart1 = Cart.objects.get(cart_id = _cart_id(request))
    myproduct = get_object_or_404(product,id=product_id)
    cart_item = Cartitem.objects.get(Product=myproduct,cart=cart1)
    cart_item.delete()
    return redirect('mycart')
