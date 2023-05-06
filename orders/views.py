import datetime
from django.shortcuts import redirect, render
from carts.models import Cartitem
from orders.models import Order
from  .forms import OrderForm

# Create your views here.
def payments(request):
    return render(request,'orders/payments.html')




def place_order(request,total = 0, quantity = 0):
    current_user = request.user

    cart_items = Cartitem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    tax = 0
    for item in cart_items:
        total += (item.Product.price*item.quantity) 
        quantity += item.quantity
    tax = (.12 * total)
    grand_total = total + tax 

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data= Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.country = form.cleaned_data['country']
            data.pincode = form.cleaned_data['pincode']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # generating order id for each order
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            data.order_number = current_date + str(data.id)
            data.save()
             
            order = Order.objects.get(user=current_user,is_ordered=False,order_number=data.order_number)
            context = {
                'order' : order,
                'cart_items' : cart_items,
                'total' : total,
                'tax' : tax,
                'grand_total' : grand_total,

            }
            return render(request,'orders/payments.html',context)
        else:
            return redirect('home')
    