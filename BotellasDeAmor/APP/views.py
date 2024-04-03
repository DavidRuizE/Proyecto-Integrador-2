from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import View
from django import forms
from django.urls import reverse
from django.shortcuts import render
from .forms import *
from .models import *
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView


# Create your views here.

class homePageView(TemplateView):
    template_name = 'core/home.html'

def loginPageView(request):
    if request.method=="POST":
        email = request.POST.get("email", "")
        password = request.POST.get("password1", "")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Ha iniciado sesión correctamente"))
            return redirect('home')
        else:
            messages.success(request, ("Hubo un error"))
            return redirect('login')
    else:
        return render(request, 'user/login.html', {})

def logoutPageView(request):
    logout(request)
    messages.success(request,(" Ha cerrado sesión exitosamente"))
    return redirect('home')


def singupView(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = request.POST["email"]
            password = request.POST["password1"]
            # Log in user
            user = authenticate(request, email=email, password=password)
            login(request, user)
            messages.success(request, "Has creado la cuenta exitosamente")
            return redirect('home')
        else:
            pass
    else:
        form = SignUpForm()

    return render(request, 'user/singup.html', {'form': form})

def uploadPhotoPageView(request):
    if request.method == 'POST':
        form = fotoForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = fotoForm()
    
    return render(request, 'photo/uploadphoto.html', {'form': form})
