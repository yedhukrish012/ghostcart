import datetime
from django.core.mail import EmailMessage
import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from accounts.models import AddressBook
from carts.models import Cartitem
from orders.models import Order, OrderProduct, Payment
from store.models import product
from  .forms import OrderForm
from django.template.loader import render_to_string

# Create your views here.
def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user = request.user,is_ordered=False,order_number=body['orderID'])
    #store transation details inside payment model
    mypayment = Payment(
        user  = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    mypayment.save()

    order.payment=mypayment
    order.is_ordered = True
    order.save()
    
    #move the cart items to order product table

    cart_item = Cartitem.objects.filter(user=request.user)

    for item in cart_item:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = mypayment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.Product_id
        orderproduct.quantity  = item.quantity
        orderproduct.product_price = item.Product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = Cartitem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variation.set(product_variation)
        orderproduct.save()

    
    #raduce quenty of sold product
        myproduct = product.objects.get(id=item.Product_id)
        myproduct.stock -= item.quantity
        myproduct.save()


    #clear cart after order placed
    Cartitem.objects.filter(user = request.user).delete()


    #send order placed resive mail

    mail_subject = 'ghostcart: Thank you for your order'
    message = render_to_string('orders/order_resive_email.html', {'user': request.user, 'order': order})
    to_email = request.user.email
    print(to_email)
    send_email = EmailMessage(mail_subject, message)
    send_email.to = [to_email]
    send_email.send()



    data = {
        'order_number': order.order_number,
        'transID': mypayment.payment_id,
    }


    return JsonResponse(data)




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

    if(request.session.get('total')):
            grand_total=request.session.get('total')

    active_Addr = AddressBook.objects.filter(user=request.user, status = True).first()

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
        

def ord_complete(request):
    myorder_number = request.GET.get('order_number')
    transationID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=myorder_number,is_ordered=True)
        ordered_product = OrderProduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id=transationID)
        subtotal = 0
        for i in ordered_product:
            subtotal += i.product_price
        context = {
            'order' : order,
            'ordered_product':ordered_product,
            'transationID':transationID,
            'payment':payment,
            'subtotal':subtotal
        }

        return render(request,'orders/ord_complete.html',context)
    except(Payment.DoesNotExist,Order.DoesNotExist):
        return redirect('home')
    






