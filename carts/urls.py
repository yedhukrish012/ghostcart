from django.urls import path
from . import views

urlpatterns = [
    path('',views.mycart,name="mycart"),
    path('add_cart/<int:product_id>/',views.add_cart,name="add_cart"),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/',views.remove_cart,name="remove_cart"),
    path('del_cart/<int:product_id>/<int:cart_item_id>/',views.del_cart,name="del_cart"),
    path('apply_coupon',views.apply_coupon,name="apply_coupon"),
    path('checkout/',views.checkout,name="checkout")
]
