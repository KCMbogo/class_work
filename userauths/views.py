from django.contrib import messages
from django.shortcuts import render, redirect
from userauths import forms
from django.contrib.auth import authenticate, login, logout
from userauths.models import User
from core.models import Customer


def register_user(request):
    
    if request.method != 'POST':
        form = forms.UserCreationForm()
    else:
        form = forms.UserCreationForm(data=request.POST)
        
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data['username']
            messages.success(request, f"Hey {username} you've successfully created an account")
            
            customer = Customer(
                user = new_user,
            )
            customer.save()
            
            new_user = authenticate(request, username=form.cleaned_data['email'],
                                     password=form.cleaned_data['password1']   
                                    )
            
            login(request, new_user)
            
            return redirect('core:index')
        else:
            messages.warning(request, form.errors)
    context = {
        'form': form
    }
    return render(request, 'userauths/register.html', context)


def login_user(request):
    
    if request.user.is_authenticated:
        return redirect("core:index")
    
    if request.method != "POST":
        form = forms.LoginForm()
    else:
        email = request.POST['email']
        password = request.POST['password']
        
        try: 
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.warning(request, f"The user with {email} doesn't exists!")
            return redirect("userauths:login")
            
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect("core:index")
        else:
            messages.warning(request, "The details do not match")
            return redirect("userauths:login")
        
    context = {
        'form': form
    }        
    return render(request, 'userauths/login.html', context)
   

def logout_user(request):
    logout(request) 
    messages.warning(request, "Logged out successfully")
    return redirect("core:index")
