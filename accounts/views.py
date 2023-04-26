from django.shortcuts import redirect, render
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
            return redirect('/verify/')
    context = {
        'form' : form
    }
    return render(request,'accounts/register.html',context)



@login_required
def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if verify.check(request.user.phone, code):
                request.user.is_verified = True
                request.user.save()
                return redirect('home')
    else:
        form = VerifyForm()
    return render(request, 'verify.html', {'form': form})


def login(request):
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['password']
             
            myuser=auth.authenticate(email=email,password=password)

            if myuser is not None:
                 auth.login(request,myuser)
                 messages.success(request,"you are now loggedin.")
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
