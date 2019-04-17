from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from .forms import UserCustomChangeForm, UserCustomCreationForm


# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserCustomCreationForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('posts:list')
            
    else:
        form = UserCustomCreationForm()
    context = {'form':form}
    return render(request, 'accounts/auth_form.html',context)
    
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.POST.get('next') or 'posts:list')
            
    else:
        form = AuthenticationForm()
        
    context = {
                'form': form,
                'next': request.GET.get('next',''),
    }
    return render(request, 'accounts/auth_form.html', context)
    
    
def logout(request):
    auth_logout(request)
    return redirect('posts:list')
  
    

def people(request, username):
    people = get_object_or_404(get_user_model(), username=username)
    context = {'people': people,}
    return render(request, 'accounts/people.html', context)
    
    
def update(request):
    if request.method == 'POST':
        form = UserCustomChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('people', request.user.username)
    else:
        form = UserCustomChangeForm(instance=request.user)
    context = {
            'form':form,
        }
    return render(request, 'accounts/auth_form.html',context)
    
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('people', request.user.username)
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form':form,
    }
    
    return render(request, 'accounts/auth_form.html', context)
    
def delete(request):
    if request.method == 'POST':
        request.user.delete()
    return redirect('posts:list')
    