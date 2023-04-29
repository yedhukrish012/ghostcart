from carts.views import _cart_id
from . models import Cart,Cartitem

def Counter(request):
    cart_count = 0
    if "admin" in request.path:
        return{}
    else:
        try:
            mycart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_items = Cartitem.objects.all().filter(cart=mycart[:1])
            for item in cart_items:
                cart_count += item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)