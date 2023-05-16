from django.db import models

# Create your models here.
class Coupon(models.Model):
    code    = models.CharField(max_length=50,unique=True)
    discount= models.PositiveIntegerField()
    min_amount  = models.IntegerField()
    active  = models.BooleanField(default=True)
    active_date = models.DateField()
    expiry_date = models.DateField()
    created_at  = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.code