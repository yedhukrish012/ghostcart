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
                return redirect('login')
    else:
        form = VerifyForm()
    return render(request, 'accounts/verify.html', {'form': form})


def login(request):
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
                      return redirect("supuser")
                 else:
                      return redirect("home")
            else:
                 messages.error(request,"invalid email or password")
                 return redirect('login')
        return render(request, 'accounts/login.html')

@login_required(login_url = "login")
def logout(request):
     auth.logout(request)
     messages.success(request,"logout sucessfully")
     return redirect("login")


def forgotpassword(request):
     return render(request,'accounts/forgotpassword.html')
