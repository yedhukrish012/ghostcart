from django.urls import include, path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signin',views.signin,name='signin'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('ver', views.verify_code,name="ver"),
    
    path('forgotpassword',views.forgotpassword,name='forgotpassword'),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name='resetpassword_validate'),
    path('resetpassword',views.resetpassword,name='resetpassword'),

    path('dashboard/',views.dashboard,name="dashboard"),
    path('myorders/',views.myorders,name="myorders"),
    path('edit_profile/',views.edit_profile,name="edit_profile"),
    path('change_password/',views.change_password,name="change_password"),
    path('order_details/<int:order_id>/',views.order_details,name="order_details"),
    
    
]