from django.urls import path, include
from . import views


app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('category', views.category, name='category'),
    path('about', views.about, name='about'),
    
    path('contact', views.contact, name='contact'),
    path('contact_us', views.contact_process, name='contact_process'),
    path('terms&policy', views.terms_policy, name='terms&policy'),
    
    path('cart', views.cart, name='cart'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('cart_action', views.cart_action, name='cart_action'),
    
    path('product-details/<int:product_id>', views.product_details, name='product_details'),
    path('checkout', views.checkout, name='checkout'),    
    
]
