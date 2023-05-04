from django.urls import include, path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signin',views.signin,name='signin'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('ver', views.verify_code,name="ver"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('forgotpassword',views.forgotpassword,name='forgotpassword'),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name='resetpassword_validate'),
    path('resetpassword',views.resetpassword,name='resetpassword'),
]