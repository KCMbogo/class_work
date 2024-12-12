from django.db import models
from djmoney.models.fields import MoneyField
from django.utils.html import mark_safe
from star_ratings.models import Rating

from userauths.models import User


def user_directory_path(instance, filename):
    return f"{instance.username}/{filename}"


class Vendor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path)
    description = models.CharField(max_length=200)
    address = models.CharField(max_length=150)
    phone_number = models.PositiveIntegerField()
    shipping_on_time = models.CharField(max_length=100, default='100')
    authentic_rating = models.CharField(max_length=100, default='100')
    days_return = models.CharField(max_length=100, default='100')
    warranty_time = models.CharField(max_length=100, default='100')
    # chat_response_time = models.DurationField(help_text='Average time taken to respond to customer chats in seconds')
    
    def vendor_image(self):
        return mark_safe("<img src='%s' width='600', height='400' />" % (self.image.url))
    
    def __str__(self) -> str:
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.name 
    

class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    old_price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', default='1000')
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def product_image(self):
        return mark_safe("<img src='%s' width='600', height='400' />" % (self.image.url))
    
    def __str__(self) -> str:
        return self.name
    
    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True, default='' )
    phone_number = models.CharField(max_length=20, blank=True, default='')
    company_name = models.CharField(max_length=100, blank=True, default='')
    town = models.CharField(max_length=100, blank=True, default='')
    district = models.CharField(max_length=100, blank=True, default='')
    postcode = models.CharField(max_length=100, blank=True, default='')
    
    def __str__(self) -> str:
        return self.user.username   
    

class Order(models.Model):
    
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SHIPPED = 'shipped', 'Shipped'
        DELIVERED = 'delivered', 'Delivered'  
        CANCELLED = 'cancelled', 'Cancelled'  
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, verbose_name='Customer')
    product = models.ManyToManyField(Product, through='OrderProduct')
    status = models.CharField(max_length=15, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    
class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Ordered By')
    quantity = models.PositiveBigIntegerField()     
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    
    def __str__(self) -> str:
        return self.product.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', default=100)
    
    def __str__(self) -> str:
         return f'{self.user.username} - {self.product.name} - {self.quantity} item(s)'


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField()    
    
    def __str__(self):
        return self.product.name


class ContactUs(models.Model):
    subject = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    message = models.TextField()
    is_email_signed = models.BooleanField()
    
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
    
    def __str__(self) -> str:
        return self.subject
    
    
    
    