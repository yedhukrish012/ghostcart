from django import forms

from store.models import ProductImage, Variation, category,product
from supuser.models import Coupon


class CategoryForm(forms.ModelForm):
    
    class Meta:
       model =  category
       fields = ["category_name","description"]

class ProductForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ["product_name", "discription", "price", "stock", "image", "is_available", "category"]
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }

    image = forms.ImageField(label='Product Image', required=True, error_messages={'required': 'Please upload an image.'})

class images(forms.ModelForm):
    model = ProductImage
    fields = ["product","image"]



class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = ["Product", "variation_category", "variation_value", "is_active"]

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount', 'min_amount', 'active', 'active_date', 'expiry_date']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'min_amount': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'active_date': forms.DateInput(attrs={'class': 'form-control datepicker mb-3'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control datepicker mb-3'})
        }