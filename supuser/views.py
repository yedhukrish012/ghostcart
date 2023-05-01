from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Account
from store.models import Variation, category,product
from supuser.forms import CategoryForm, ProductForm, VariationForm

# Create your views here.
def supuser(request):
    return render(request,'supuser/suphome.html')


#----------------------------------USER-MANAGE-ADMIN-side----------------------------------------------------------------------------------------

def usermanage(request):
    users = Account.objects.filter(is_superadmin=False).order_by('id').reverse()
    context = {
        'users': users,
    }
    return render(request,'supuser/customer.html',context)

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
    categories = category.objects.all()
    context = {
       "category": categories
    }
    return render(request, 'supuser/category.html', context)


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



def productmanage(request):
    Products = product.objects.all()
    context = {
        "Products" : Products 
    }
    return render(request, 'supuser/products.html', context)

def add_product(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return redirect('productmanage')
    else:
        product_form = ProductForm()
    context = {
        "product_form" : product_form
    }
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
    variations = Variation.objects.all()
    context = {
        "variations" : variations
    }
    return render(request, 'supuser/Variation.html', context)

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










