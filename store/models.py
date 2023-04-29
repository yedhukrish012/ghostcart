from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse

# Create your models here.
class category(models.Model):
    category_name = models.CharField(max_length=50,unique=True)
    slug = models.CharField(max_length=100,unique=True)
    description = models.CharField(max_length=255,blank=True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('product_by_category',args = [self.slug])


    def __str__(self):
        return self.category_name



class product(models.Model):
    product_name = models.CharField(max_length=200,unique=True)
    slug         = models.SlugField(max_length=200,unique=True)
    discription  = models.TextField(max_length=500,blank=True)
    price        = models.IntegerField()
    stock        = models.IntegerField()
    image        = models.ImageField(upload_to='photos/producs')
    is_available  =models.BooleanField(default=True)
    category      =models.ForeignKey(category,on_delete=models.CASCADE)

    def get_url(self):
        return reverse('product_details',args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
    




class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active=True)
    
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)

    
variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)    
    
class Variation(models.Model):
    Product = models.ForeignKey(product,on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100,choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
    