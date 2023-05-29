import datetime
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from accounts.models import AddressBook
from supuser.models import Coupon
from . models import Cart, Cartitem
from store.models import Variation, product
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.
def mycart(request,total = 0, quantity = 0, cart_items = None):
    tax = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = Cartitem.objects.filter(user=request.user,is_active=True)
        else:
            mycart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cartitem.objects.filter(cart=mycart,is_active=True)
        for item in cart_items:
            if item.Product.offer_price:
                total += (item.Product.offer_price * item.quantity)
            else:
                total += (item.Product.price * item.quantity)
            quantity += item.quantity
        tax = int(.12 * total)
        grand_total = total + tax    
    except ObjectDoesNotExist:
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
    current_user = request.user
    myproduct = product.objects.get(id=product_id)
    if current_user.is_authenticated:
        variation_products = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                
                try:
                    variation = Variation.objects.get(Product=myproduct,variation_category__iexact=key,variation_value__iexact=value)
                    variation_products.append(variation)
                except:
                    pass
    
        is_cart_item_exists =Cartitem.objects.filter(Product=myproduct,user=current_user).exists()
        if is_cart_item_exists:
            cart_item = Cartitem.objects.filter(Product=myproduct, user=current_user)
            existing_variation_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)

            if variation_products in existing_variation_list:
                index = existing_variation_list.index(variation_products)
                item_id = id[index]
                item = Cartitem.objects.get(Product = myproduct,id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = Cartitem.objects.create(Product=myproduct,quantity=1,user=current_user)
                if len(variation_products) > 0:
                    item.variations.clear()
                    item.variations.add(*variation_products)
                item.save()
        else:
            cart_item = Cartitem.objects.create(
                Product = myproduct,
                quantity = 1,
                user=current_user,
            )
            if len(variation_products) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*variation_products)
            cart_item.save()
        return redirect('mycart')


    else:
        variation_products = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                
                try:
                    variation = Variation.objects.get(Product=myproduct,variation_category__iexact=key,variation_value__iexact=value)
                    variation_products.append(variation)
                except:
                    pass
        try:
            mycart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            mycart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        mycart.save()


        is_cart_item_exists =Cartitem.objects.filter(Product=myproduct,cart=mycart).exists()
        if is_cart_item_exists:
            cart_item = Cartitem.objects.filter(Product=myproduct, cart=mycart)
            existing_variation_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)

            if variation_products in existing_variation_list:
                index = existing_variation_list.index(variation_products)
                item_id = id[index]
                item = Cartitem.objects.get(Product = myproduct,id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = Cartitem.objects.create(Product=myproduct,quantity=1,cart=mycart)
                if len(variation_products) > 0:
                    item.variations.clear()
                    item.variations.add(*variation_products)
                item.save()
        else:
            cart_item = Cartitem.objects.create(
                Product = myproduct,
                quantity = 1,
                cart = mycart,
            )
            if len(variation_products) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*variation_products)
            cart_item.save()
        return redirect('mycart')






def remove_cart(request,product_id,cart_item_id):
    
    myproduct = get_object_or_404(product,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = Cartitem.objects.get(Product=myproduct,user=request.user,id=cart_item_id)
        else:
            mycart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = Cartitem.objects.get(Product=myproduct,cart=mycart,id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('mycart')

def del_cart(request,product_id,cart_item_id):
    
    myproduct = get_object_or_404(product,id=product_id)
    if request.user.is_authenticated:
        cart_item = Cartitem.objects.get(Product=myproduct,user=request.user,id=cart_item_id)
    else:
        cart1 = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = Cartitem.objects.get(Product=myproduct,cart=cart1,id=cart_item_id)
    cart_item.delete()
    return redirect('mycart')


@login_required(login_url='signin')
def checkout(request):
    total=0
    quantity= 0
    cart_items=None
    tax = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = Cartitem.objects.filter(user=request.user,is_active=True)
        else:
            mycart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cartitem.objects.filter(cart=mycart,is_active=True)
        for item in cart_items:
            if item.Product.offer_price:
                total += (item.Product.offer_price * item.quantity)
            else:
                total += (item.Product.price * item.quantity)
            quantity += item.quantity
        tax = int(.12 * total)
        grand_total = total + tax 

        if(request.session.get('total')):
            grand_total=request.session.get('total')

        addresses = AddressBook.objects.filter(user=request.user).order_by('-id')
        cadd = AddressBook.objects.filter(user=request.user, status= True).first()

    except :
        pass
    context = {

        'total':total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total' : grand_total,
        'addresses':addresses,
        'cadd':cadd,

               }
    return render(request,'store/checkout.html',context)



@require_POST
def apply_coupon(request):
    body = json.loads(request.body)
    grand_total = int(body['grand_total'])
    coupon_code = body['coupon']
    try:
        coupon = Coupon.objects.get(code__iexact=coupon_code)
    except Coupon.DoesNotExist:
        data = {
            "total": grand_total,
            "message": "Not a Valid Coupon"
        }
    else:
        today = datetime.now().date()
        start_date = coupon.active_date
        expiry_date = coupon.expiry_date
        min_amount = int(coupon.min_amount)
        if min_amount < grand_total and start_date <= today <= expiry_date:
            grand_total -= int(coupon.discount)
            request.session['total'] = grand_total
            data = {
                "total": grand_total,
                "message": f"{coupon.code} Applied"
            }
        else:
            data = {
                "total": grand_total,
                "message": "Not a Valid Coupon"
            }
    return JsonResponse(data)