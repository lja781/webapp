from django.contrib.auth import login as func_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout as func_logout
from django.shortcuts import render, redirect

from mysite.site_functions import generate_meta

def login(request):
    meta = generate_meta(request)
    if request.user.is_authenticated:
        return redirect('profile')
    elif request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                func_login(request, user)
                return redirect('home')
    form = AuthenticationForm(request)
    return render(request, 'accounts/login.html', {'form':form, 'meta':meta})

def signup(request):
    meta = generate_meta(request)
    if request.user.is_authenticated:
        return redirect('profile')
    elif request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            func_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form, 'meta':meta})

def profile(request):
    meta = generate_meta(request)
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    return render(request, 'accounts/profile.html', {'meta':meta, 'user':user})

def logout(request):
    meta = generate_meta(request)
    meta["is_logged_in"]=False
    if request.user.is_authenticated:
        func_logout(request)
    else:
        return redirect('home')
    return render(request, 'accounts/logout.html', {'meta':meta})

def cv(request):
    meta = generate_meta(request)
    return render(request, 'accounts/cv.html', {'meta':meta})

def cv_edit(request):
    meta = generate_meta(request)
    return render(request, 'accounts/cv_edit.html', {'meta':meta})
