from django.shortcuts import get_object_or_404, redirect, render

from carts.models import Cart, Cartitem
from carts.views import _cart_id
from orders.models import Order, OrderProduct
from . import verify
from . models import Account, UserProfile
from django.contrib import auth, messages
from store.models import Wishlist, product
from . forms import UserForm, VerifyForm, registration,UserProfileForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required


from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import requests

# Create your views here.
def home(request):
    
    products = product.objects.all().filter(is_available = True)
    context = {
        "products" : products
    }
    return render(request,'accounts/index.html',context)



def register(request):
    form = registration()
    if request.method == 'POST':
        form = registration(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password1 = form.cleaned_data['password1']
            user = Account.objects.create_user(first_name = first_name, last_name = last_name, phone_number = phone_number, email = email, password = password1)
            user.save()
            request.session['email']=email
            
            verify.send(phone_number)
            messages.success(request,"Registered Sucessfully! Verify OTP to Continue")
            return redirect('ver')
    context = {
        'form' : form
    }
    return render(request,'accounts/register.html',context)




def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            user = Account._default_manager.get(email=request.session.get('email'))
            if verify.check(user.phone_number, code):
                user.is_active = True
                user.is_verified = True
                user.save()
                return redirect('signin')
    else:
        form = VerifyForm()
    return render(request, 'accounts/verify.html', {'form': form})


def signin(request):
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['password']
             
            myuser=auth.authenticate(email=email,password=password)

            if myuser is not None:
                 
                 try:
                    mycart = Cart.objects.get(cart_id=_cart_id(request)) 
                    is_cart_item_exists =Cartitem.objects.filter(cart=mycart).exists()
                    if is_cart_item_exists:
                         cart_item = Cartitem.objects.filter(cart=mycart)
                         variation_products = []
                         for item in cart_item:
                              variation = item.variations.all()
                              variation_products.append(list(variation))

                        #get the cart cart items to access the user product variations
                         cart_item = Cartitem.objects.filter(user=myuser)
                         existing_variation_list = []
                         id = []
                         for item in cart_item:
                             existing_variation = item.variations.all()
                             existing_variation_list.append(list(existing_variation))
                             id.append(item.id)


                         for vp in variation_products:
                              if vp in existing_variation_list:
                                  index=existing_variation_list(vp)
                                  item_id = id[index]
                                  item = Cartitem.objects.get(id=item_id)
                                  item.quantity += 1
                                  item.user = myuser
                                  item.save()
                              else:
                                  cart_item = Cartitem.objects.filter(cart=mycart)
                                  for item in cart_item:
                                    item.user = myuser
                                    item.save()

                         
                 except:
                      pass
    
                 auth.login(request,myuser)
                 messages.success(request,"you are now loggedin.")
                 if myuser.is_superadmin:
                      request.session['email'] = email
                      return redirect("supuser")
                 else:
                      url = request.META.get('HTTP_REFERER')
                      return redirect("home")
            else:
                 messages.error(request,"invalid email or password")
                 return redirect('signin')
        return render(request, 'accounts/login.html')

@login_required(login_url = "signin")
def logout(request):
     if 'email' in request.session:
         request.session.flush
     auth.logout(request)
     messages.success(request,"logout sucessfully")
     return redirect("signin")

@login_required(login_url='signin')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    ordercount=orders.count()
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context={
        'ordercount':ordercount,
        'userprofile':userprofile
    }
    return render(request,'accounts/dashboard.html',context)



def forgotpassword(request):
     if request.method == "POST":
         email = request.POST['email']
         if Account.objects.filter(email=email).exists():
             user =Account.objects.get(email__exact=email)

             current_site =get_current_site(request)
             mail_subject = 'ghostcart : Reset your password'
             message = render_to_string( 'accounts/reset_account_password.html', {
                'user': user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
                })
             to_email = email
             print(to_email)
             send_email = EmailMessage(mail_subject,message,to=[to_email])
             send_email.send()
             messages.success(request, 'Password reset email has been sent to your email address')
             return redirect('signin')
         else:
             messages.error(request,"Account Does't Exists!!!")
             return redirect('forgotpassword')
     return render(request,'accounts/forgotpassword.html')

def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError,OverflowError, Account.DoesNotExist):
        user = None
    
    if user  is not None and default_token_generator.check_token(user, token):
        request.session['uid']= uid
        messages.success(request,'Please reset your password.!')
        return redirect('resetpassword')
    else:
        messages.error(request, 'Sorry, the activation link has expired.!')
        return redirect('signin')
    
def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,"sucessfully reset password")
            return redirect('signin')

        else:
            messages.error(request,"Passwords are not match")
            return redirect('resetpassword')
    else:
     return render(request,'accounts/resetpassword.html')

@login_required(login_url='signin')    
def myorders(request):
    orders = Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    context={
        'orders': orders
    }
    return render(request,'accounts/myorders.html',context)

@login_required(login_url='signin')    
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST,request.FILES,instance=userprofile)
        if user_form.is_valid and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,"Your profile has been Updated.")
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        "user_form" : user_form,
        "profile_form" : profile_form,
        "userprofile" : userprofile
    }
    return render(request,'accounts/edit_profile.html',context)

@login_required(login_url='signin')
def change_password(request):
    if request.method == 'POST':
        currentpassword = request.POST['current_password']
        newpassword = request.POST['new_password']
        conformpassword = request.POST['conform_password']

        myuser = Account.objects.get(email__exact=request.user.email)

        if newpassword == conformpassword:
            success = myuser.check_password(currentpassword)
            if success:
                myuser.set_password(newpassword)
                myuser.save()
                messages.success(request,'password updated sucessfully')
                return redirect('change_password')
            else:
                messages.error(request,'Current Password is invalid!!!')
                return redirect('change_password')
        else:
            messages.error(request,"Password Does't Match")
            return redirect('change_password')
    return render(request,'accounts/change_password.html')


@login_required(login_url='signin')
def order_details(request, order_id):
    try:
        ordr_product = OrderProduct.objects.filter(order__order_number=order_id)
        order = Order.objects.get(order_number=order_id)
        subtotal = 0
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
    
    return render(request, 'accounts/order_details.html', context)


@login_required(login_url='signin')
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'store/wishlist.html',context)


@login_required(login_url='signin')
def add_to_wishlist(request, product_id):
    myproduct = get_object_or_404(product, id=product_id)
    created = Wishlist.objects.get_or_create(user=request.user, product=myproduct)
    if created:
        # Wishlist item was added successfully
        messages.success(request, 'Product added to wishlist.')
    else:
        # Wishlist item already exists
        messages.info(request, 'Product already in wishlist.')
    return redirect('wishlist')



@login_required(login_url='signin')
def remove_from_wishlist(request, product_id):
    myproduct = get_object_or_404(product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=myproduct).delete()
    messages.success(request, 'Product removed from wishlist.')
    return redirect('wishlist')

