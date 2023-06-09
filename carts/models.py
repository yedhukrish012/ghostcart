from django.db import models
from accounts.models import Account

from store.models import Variation, product

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class Cartitem(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE, null=True)
    Product = models.ForeignKey(product,on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart    = models.ForeignKey(Cart,on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        if self.Product.offer_price:
            return self.Product.offer_price * self.quantity
        else:
            return self.Product.price * self.quantity

    def __unicode__(self):
        return self.Product
    