from django.contrib.auth import login as func_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout as func_logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from .forms import *
from .models import *
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

def cv_pk(request, pk):
    meta = generate_meta(request)
    user = request.user
    cv = get_object_or_404(CV, pk=pk)
    return render(request, 'accounts/cv.html', {'meta':meta, 'cv':cv})

def cv(request):
    pk = User.objects.filter(is_superuser=True).first().pk
    return cv_pk(request, pk)

def cv_edit(request, pk):
    meta = generate_meta(request)
    cv = get_object_or_404(CV, pk=pk)
    if request.user != cv.owner:
        return redirect('cv_pk', pk=pk)

    referees = cv.referee_set.all()
    addresses = cv.addresscv_set.all()
    educations = cv.education_set.all()
    tech_skills = cv.techskill_set.all()
    work_experiences = cv.workexperience_set.all()
    if request.method == "POST":
        cv_form = CVForm(request.POST, instance=cv)
        referee_forms = [RefereeForm(request.POST, prefix=str(x), instance=v) for x,v in enumerate(referees)]
        address_forms = [AddressCVForm(request.POST, prefix=str(x), instance=v) for x,v in enumerate(addresses)]
        education_forms = [EducationForm(request.POST, prefix=str(x), instance=v) for x,v in enumerate(educations)]
        tech_skill_forms = [TechSkillForm(request.POST, prefix=str(x), insance=v) for x,v in enumerate(tech_skills)]
        work_experience_forms = [WorkExperienceForm(request.POST, prefix=str(x), instance=v) for x,v in enumerate(work_experiences)]
        all_list = [cv_form] + referee_forms + address_forms + education_forms + tech_skill_forms + work_experience_forms
        if all([f.is_valid() for f in all_list]):
            cv = cv_form.save(commit=False)
            def saver(l):
                for f in l:
                    o = f.save(commit=False)
                    o.save()
            saver(referee_forms)
            saver(address_forms)
            saver(education_forms)
            saver(tech_skill_forms)
            saver(work_experience_forms)
            cv.save()
            return redirect('cv_pk', pk=pk)
    else:
        cv_form = CVForm(instance=cv)
        referee_forms = [RefereeForm(prefix=str(x), instance=v) for x,v in enumerate(referees)]
        address_forms = [AddressCVForm(prefix=str(x), instance=v) for x,v in enumerate(addresses)]
        education_forms = [EducationForm(prefix=str(x), instance=v) for x,v in enumerate(educations)]
        tech_skill_forms = [TechSkillForm(prefix=str(x), insance=v) for x,v in enumerate(tech_skills)]
        work_experience_forms = [WorkExperienceForm(prefix=str(x), instance=v) for x,v in enumerate(work_experiences)]
    return render(request, 'accounts/cv_edit.html', {'meta':meta, 'cv_form':cv_form, 'referee_forms':referee_forms, 'address_forms':address_forms, 'education_forms':education_forms, 'tech_skill_forms':tech_skill_forms, 'work_experience_forms':work_experience_forms})
