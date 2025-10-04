from django.urls import path
from cart import views

app_name = 'cart'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('delete_cart_item/', views.delete_cart_item, name='delete_cart_item'),
    
    path('create_product/', views.create_product, name='create_product'),
    path('update_product/<id>/', views.update_product, name='update_product'),

    path("delete_variants/<product_id>/<variant_id>/", views.delete_variants, name="delete_variants"),
    path("delete_variants_items/<variant_id>/<item_id>/", views.delete_variants_items, name="delete_variants_items"),

    path("delete_product_image/<product_id>/<image_id>/", views.delete_product_image, name="delete_product_image"),
    path("delete_product/<product_id>/", views.delete_product, name="delete_product")

    
]