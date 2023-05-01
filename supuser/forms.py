from django import forms

from store.models import Variation, category,product


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



class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = ["Product", "variation_category", "variation_value", "is_active"]