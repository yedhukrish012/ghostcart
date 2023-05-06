from django.shortcuts import redirect, render

from carts.models import Cart, Cartitem
from carts.views import _cart_id
from . import verify
from . models import Account
from django.contrib import auth, messages
from store.models import product
from . forms import VerifyForm, registration
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

def dashboard(request):
    return render(request,'accounts/dashboard.html')



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
    
