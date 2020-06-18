from django.contrib.auth import login as func_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout as func_logout
from django.shortcuts import render, redirect

def login(request):
    meta = {"is_logged_in":request.user.is_authenticated}
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
            else:
                pass
                #return redirect("")
    form = AuthenticationForm(request)
    return render(request, 'accounts/login.html', {'form':form, 'meta':meta})

def signup(request):
    meta = {"is_logged_in":request.user.is_authenticated}
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
    meta = {"is_logged_in":request.user.is_authenticated}
    user = {"username":request.user.username}
    return render(request, 'accounts/profile.html', {'meta':meta, 'user':user})

def logout(request):
    meta = {"is_logged_in":False}
    if request.user.is_authenticated:
        func_logout(request)
    else:
        return redirect('home')
    return render(request, 'accounts/logout.html', {'meta':meta})
