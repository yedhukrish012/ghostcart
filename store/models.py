from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from accounts.models import Account


# Create your models here.
class category(models.Model):
    category_name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    description = models.CharField(max_length=255,blank=True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name



class product(models.Model):
    product_name = models.CharField(max_length=200,unique=True)
    slug         = models.SlugField(max_length=200,unique=True)
    discription  = models.TextField(max_length=500,blank=True)
    price        = models.IntegerField()
    stock        = models.IntegerField()
    image        = models.ImageField(upload_to='photos/products')
    is_available  =models.BooleanField(default=True)
    category      =models.ForeignKey(category,on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name
    
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
            i = 1
            while product.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.product_name)}-{i}"
                i += 1
        super().save(*args, **kwargs)

    def get_url(self):
        return reverse('product_details',args=[self.category.slug, self.slug])
    

    def get_image_upload_path(instance, filename):
        # Generate a unique filename for each uploaded image
        return 'photos/products/{0}/{1}'.format(instance.slug, filename)

   

    # Main product image
    image = models.ImageField(upload_to=get_image_upload_path)


    # existing methods...

class ProductImage(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/products')

    def __str__(self):
        return self.image.url
    

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

class ReviewRating(models.Model):
    products = models.ForeignKey(product,on_delete=models.CASCADE)
    user  = models.ForeignKey(Account,on_delete=models.CASCADE)
    subject = models.CharField(max_length=100,blank=True)
    review = models.TextField(max_length=500,blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20,blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
    