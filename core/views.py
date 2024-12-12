from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import AddToCartForm, ReviewForm
from django.contrib import messages
from django.db.models import Avg
from django_countries import countries
from django.contrib.auth.decorators import login_required
from djmoney.money import Money
from star_ratings.models import Rating
import requests


def index(request):
    categories = Category.objects.all()
    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    
    tabs = ['one', 'two', 'three', 'four', 'five']
    
    products = Product.objects.all().order_by('-created_at')
    
    comparison_amount = Money(100, 'USD')
    
    context = {
        'zipped_data': zip(categories, tabs),
        'products': products,
        'categories': categories,
        'cart_items': cart_items,
        'comparison_amount': comparison_amount,
    }
    return render(request, 'core/index.html', context)


def category(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    
    selected_categories = request.GET.getlist('categories')
    
    if 'all' in selected_categories:
        products = Product.objects.all().order_by('-created_at')
    else:
        products = Product.objects.filter(category__id__in=selected_categories)
    
    context = {
        'categories': categories,
        'products': products,
        'cart_items': cart_items,
    }
    return render(request, 'core/category.html', context)


def about(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    categories = Category.objects.all()
    
    context = {
        'cart_items': cart_items,
        'categories': categories,
    }
    return render(request, 'core/about.html', context)


def contact(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    categories = Category.objects.all()
    context = {'cart_items': cart_items, 'categories': categories}
    return render(request, 'core/contact.html', context)


def contact_process(request):
    if request.method == 'POST':
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        is_email_signed = False
        
        if request.user.is_authenticated and request.user.email == email:
            is_email_signed = True
    
        ContactUs.objects.create (
            subject = subject,
            email = email,
            message = message,
            is_email_signed = is_email_signed
        )
    
    return redirect('core:contact')


def terms_policy(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    categories = Category.objects.all()
    context = {'cart_items': cart_items, 'categories': categories}
    return render(request, 'core/terms&policy.html', context)



@login_required()
def product_details(request, product_id):
    
    product = Product.objects.get(id=product_id)
    
    form = AddToCartForm(initial={'product_id': product_id})
    
    category = product.category
    
    category_products = Product.objects.filter(category=category)
    
    ratings = Rating.objects.for_instance(product)
    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    
    categories = Category.objects.all()

    if request.method != 'POST':
        review_form = ReviewForm(initial={'user': request.user, 'product': product, 'rating': ratings})
    else:
        review_form = ReviewForm(request.POST)
        
        if review_form.is_valid():
            if request.user == review_form.cleaned_data['user']:
                pass
            else:
                review_form.save()
                
    reviews = Review.objects.filter(product=product)
                
    review_count = reviews.count()
    
    context = {
        'product': product,
        'cat_products': category_products,
        'form': form,
        'cart_items': cart_items,
        'categories': categories,
        'ratings': ratings,
        'review_form': review_form,
        'review_count': review_count,
    }
    return render(request, 'core/product-details.html', context)



@login_required()
def cart(request): 
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
        
    categories = Category.objects.all()
    
    subtotal = 0
    for item in cart_items:
        subtotal += item.total
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'categories': categories,
    }
    
    return render(request, 'core/cart.html', context)



def add_to_cart(request):
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            quantity = form.cleaned_data['quantity']
            product = get_object_or_404(Product, id=product_id)
            total = quantity * product.price

            # Add product to the cart
            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={
                    'quantity': quantity,
                    'total': total,
                }
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return redirect('core:cart')
        
    return redirect('core:product_details')



def cart_action(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update':
            # iterating through the form data
            for key, value in request.POST.items():
                if key.startswith('quantity_'):
                    cart_item_id = int(key.split('_')[1]) 
                    if request.user.is_authenticated:
                        cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
                    else:
                        cart_item = None
                                    
                    new_quantity = int(value)
                    
                    if new_quantity > 0:
                        cart_item.quantity = new_quantity
                        cart_item.total = new_quantity * cart_item.product.price
                        cart_item.save()
                    else:
                        cart_item.delete()
                        
            return redirect('core:cart')
        
        elif action == 'delete':
            del_id = request.POST.get('del_id')
            
            if request.user.is_authenticated and request.method == 'POST':
                cart_item = Cart.objects.get(id=del_id, user=request.user)
                cart_item.delete()
            else:
                cart_items = None
                messages.success(request, 'Successfully deleted')
            
                return redirect('core:cart')
            return redirect('core:cart')
        
        elif action == 'clear':
            if request.user.is_authenticated and request.method == 'POST':
                Cart.objects.filter(user=request.user).delete()
                
                messages.success(request, 'Successfully cleared the cart!')
                return redirect('core:cart')
    


@login_required()
def checkout(request):
    categories = Category.objects.all()
    cart_items = Cart.objects.filter(user=request.user)
    subtotal = sum(item.total for item in cart_items)
    deliver_cost = Money(0, 'USD')

    if request.method == 'POST':
        user = request.user
        phone_number = request.POST['phone_number']
        company = request.POST.get('company', '')
        country = request.POST['country']
        address = request.POST['address']
        town = request.POST['city']
        district = request.POST['district']
        postcode = request.POST['zip']
        deliver = request.POST['deliver']
        
        if deliver:
            deliver_cost = Money(500, 'USD')

        # Ensure the customer is created or updated
        customer, created = Customer.objects.get_or_create(user=user)
        customer.phone_number = phone_number
        customer.company_name = company
        customer.country = country
        customer.address = address
        customer.town = town
        customer.district = district
        customer.postcode = postcode
        customer.save()

        # Create the order
        order = Order.objects.create(user=user)

        # Create OrderProduct entries
        for item in cart_items:
            OrderProduct.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        
        # Calculate total
        total = subtotal + deliver_cost

        # Redirect to payment processing
        # return redirect('core:checkout')

    context = {
        'categories': categories,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'deliver_cost': deliver_cost,
        'total': subtotal + deliver_cost,
    }
    return render(request, 'core/checkout.html', context)

