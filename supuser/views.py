from django.forms import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Account
from store.models import ProductImage, Variation, category,product
from supuser.forms import CategoryForm, ProductForm, VariationForm, images

# Create your views here.
def supuser(request):
    if 'email' in request.session:
        return render(request,'supuser/suphome.html')
    return redirect('signin')


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










