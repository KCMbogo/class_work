from django.contrib import admin
from .models import *

class VendorAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'phone_number']
    
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']   
    
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price']   
    
    
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'phone_number']  
    
     
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'get_rating_field')  
    
    def get_rating_field(self, obj):
        return obj.rating.count
    
     
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'order']  
    
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'created_at']  
    
    
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['email', 'subject'] 
    
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
