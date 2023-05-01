from django.urls import path
from . import views

urlpatterns = [
    path('',views.supuser,name="supuser"),
    path('manage/', views.usermanage, name='manage'),
    path('manage/block/<int:id>/',views.block_user, name='block_user'),
    path('manage/unblock/<int:id>/',views.unblock_user, name='unblock_user'),

    path('caregotys/', views.categorymanage, name='categorymanage'),
    path('Category/add/', views.add_category, name='add_category'),
    path('Category/del/<int:id>', views.del_category, name='del_category'),

    path('productmanage/',views.productmanage,name="productmanage"),
    path('productmanage/add/',views.add_product,name="add_product"),
    path('productmanage/edit/<int:id>',views.edit_product,name="edit_product"),
    path('productmanage/del/<int:id>', views.del_product, name='del_product'),

    path('Variationmanage/',views.Variationmanage,name="Variationmanage"),
    path('Variationmanage/add',views.add_variation,name="add_variation"),
    path('Variationmanage/edit<int:id>',views.edit_variation,name="edit_variation"),
    path('Variationmanage/del<int:id>',views.del_variation,name="del_variation"),

]