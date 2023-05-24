
import json
from django.forms import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from  django.core import serializers
from accounts.models import Account
from orders.models import Order, OrderProduct
from store.models import ProductImage, Variation, category,product
from supuser.forms import CategoryForm, CouponForm, ProductForm, VariationForm, images
from datetime import datetime,timedelta, timezone
from django.db.models import Q

from supuser.models import Coupon

# Create your views here.
def supuser(request):
    if 'email' in request.session:
        orders = Order.objects.all().order_by('-created_at')[:5]
    
        users = Account.objects.all()
        users_count = users.count()

        myproducts = product.objects.all().order_by('-id')
    
        categories = category.objects.all()
        category_count = categories.count()
    
        total_order = Order.objects.all()
        total_orders = total_order.count()
    
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        dates = [start_of_week + timedelta(days=i) for i in range(7)]
        sales = []
        for date in dates:
            Orders = OrderProduct.objects.filter(
                ordered=True,
                created_at__year=date.year,
                created_at__month=date.month,
                created_at__day=date.day,
            )
            total_sales = sum(order.product_price * order.quantity for order in Orders)
            sales.append(total_sales)
        sums = sum(sales)
        product_count = myproducts.exclude(orderproduct__ordered=True).count()
        context = {
            'orders': orders,
            'product_count': product_count,
            'category_count': category_count,
            'products': myproducts,
            'total_orders': total_orders,
            "users_count": users_count,
            'dates': dates,
            'sales': sales,
            'sums': sums,
        }
        return render(request, 'supuser/suphome.html', context)
    else:
        return redirect('signin')

    

    
def add_order_filter(request):
    body = json.loads(request.body)
    try:
        start_date =datetime.strptime(body['from'],'%Y-%m-%d')
        end_date = datetime.strptime(body['to'],'%Y-%m-%d')
    except ValueError:
        end_date = timezone.now()
        start_date = end_date - timedelta(days=end_date.weekday())
    try:
        orders = Order.objects.filter(created_at__gte=start_date, created_at__lte=end_date)
        json_data = serializers.serialize('json', orders)
    except Order.DoesNotExist:
        orders = None     
    data ={
             "order":json_data,
            }
    return JsonResponse(data)
#----------------------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------USER-MANAGE-ADMIN-side----------------------------------------------------------------------------------------

def usermanage(request):
    if 'email' in request.session:
        users = Account.objects.filter(is_superadmin=False).order_by('id').reverse()
        context = {
            'users': users,
        }
        return render(request,'supuser/customer.html',context)
    return redirect('signin')

def block_user(request,id):
    if request.method == 'POST':
        pi = Account.objects.get(id=id)
        pi.is_active=False
        pi.save()
        return redirect('manage')
    
def unblock_user(request,id):
    if request.method == 'POST':
        pi = Account.objects.get(id=id)
        pi.is_active=True
        pi.save()
        return redirect('manage')
    
#---------------------------------------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------CATEGOTY-MANAGE-------------------------------------------------------------------------------

def categorymanage(request):
    if 'email' in request.session:
        categories = category.objects.all()
        context = {
        "category": categories
        }
        return render(request, 'supuser/category.html', context)
    return redirect('signin')


def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorymanage')
    else:
        form = CategoryForm()
    context = {
        "form": form
    }
    return render(request, 'supuser/add_category.html', context)


def del_category(request,id):
    if request.method == "POST":
        crt = category.objects.get(id=id)
        crt.delete()
    return redirect('categorymanage')

#----------------------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------product-manage--------------------------------------------------------------------------------------------

def productmanage(request):
    if 'email' in request.session:
        Products = product.objects.all()
        context = {
            "Products" : Products 
        }
        return render(request, 'supuser/products.html', context)
    return redirect('signin')



# ProductImageFormSet = inlineformset_factory(product, ProductImage, form=images, extra=3)
ProductImageFormSet = inlineformset_factory(product, ProductImage, form=images, extra=3, fields=['image'])



def add_product(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        image_form = ProductImageFormSet(request.POST, request.FILES, instance=product())
        if product_form.is_valid() and image_form.is_valid():
            myproduct = product_form.save(commit=False)
            myproduct.save()
            image_form.instance = myproduct
            image_form.save()
            return redirect('productmanage')
    else:
        product_form = ProductForm()
        image_form = ProductImageFormSet(instance=product())
    
    context = {'product_form': product_form, 'image_form': image_form}
    return render(request, 'supuser/add_product.html', context)
   
   

def del_product(request,id):
    if request.method == "POST":
        prod = product.objects.get(id=id)
        prod.delete()
    return redirect('productmanage')



def edit_product(request, id):
    Product = get_object_or_404(product, id=id)
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES, instance=Product)
        if product_form.is_valid():
            product_form.save()
            return redirect('productmanage')
    else:
        product_form = ProductForm(instance=Product)

    context = {
        "product_form": product_form
    }
    return render(request, 'supuser/edit_product.html', context)


#-------------------------------------------------------------------------------------------------------------------------------------------------------------


#--------------------------------------------------VARIATION-MANAGE-----------------------------------------------------------------------------------------------------

def Variationmanage(request):
    if 'email' in request.session:
        variations = Variation.objects.all()
        context = {
            "variations" : variations
        }
        return render(request, 'supuser/Variation.html', context)
    return redirect('signin')

def add_variation(request):
    if request.method == "POST":
        variationform = VariationForm(request.POST)
        if variationform.is_valid():
            variationform.save()
            return redirect('Variationmanage')
    else: 
        variationform = VariationForm()   
    context = {
        "variationform": variationform
    }
    return render(request, 'supuser/add_variation.html', context)

def edit_variation(request,id):
    vari = get_object_or_404(Variation, id=id)
    if request.method == "POST":
        variationform = VariationForm(request.POST,instance=vari)
        if variationform.is_valid():
            variationform.save()
            return redirect('Variationmanage')
    else:
        variationform = VariationForm(instance=vari)
    context = {
        "variationform" : variationform
    }
    return render(request, 'supuser/edit_variation.html', context)

def del_variation(request,id):
    if request.method == "POST":
        vari = Variation.objects.get(id=id)
        vari.delete()
    return redirect('Variationmanage')

#----------------------------------------------------------------------------------------------------------------------------------------------------------




def orderslist(request):
    orders = Order.objects.all().order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'supuser/orders_list.html', context)



def order_details_admin(request, order_id):
    try:
        subtotal = 0
        ordr_product = OrderProduct.objects.filter(order__order_number=order_id)
        order = Order.objects.get(order_number=order_id)
        for i in ordr_product:
            subtotal += i.product_price*i.quantity
        context = {
            'ordr_product': ordr_product,
            'order': order,
            'subtotal' : subtotal
        }
    except Order.DoesNotExist:
        # Handle the case when the order does not exist
        context = {
            'error_message': 'Order does not exist.'
        }
    
    return render(request, 'supuser/order_details_admin.html', context)




def change_status(request, order_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        try:
            order = Order.objects.get(id=order_id)
            order.status = status
            order.save()
        except Order.DoesNotExist:
            pass
    
    return redirect('orderslist')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------Couppen--Management--------------------------------------------------------------------------------------------------------------------------------

def coupen_manage(request):
    coupens = Coupon.objects.all()
    context = {
        "coupens" : coupens
    }
    return render(request,'supuser/coupen_manage.html', context)



def add_coupons(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coupen_manage')
    else:
        form = CouponForm()

    context = {'form': form}
    return render(request, 'supuser/add_coupons.html', context)



def del_coupons(request,id):
    if request.method == "POST":
        coup = Coupon.objects.get(id=id)
        coup.delete()
    return redirect('coupen_manage')


def edit_coupons(request,id):
    if request.method == "POST":
        coup = Coupon.objects.get(id=id)
        form = CouponForm(request.POST, instance=coup)
        if form.is_valid:
            form.save()
        return redirect('coupen_manage')
    else:
        coup = Coupon.objects.get(id=id)
        form = CouponForm(instance=coup)
        context = {
            "form" : form
        }
    return render(request, 'supuser/edit_coupon.html', context)
    















