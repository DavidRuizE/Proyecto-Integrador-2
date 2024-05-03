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


def homePageView(request):
    filter_option = request.GET.get('filter')
    name_query = request.GET.get('name')
    photo_type_query = request.GET.get('photoType')

    photos = Foto.objects.all()

    if filter_option == 'recent':
        photos = photos.order_by('-date')
    elif filter_option == 'oldest':
        photos = photos.order_by('date')

    if name_query:
        photos = photos.filter(name__icontains=name_query)

    if photo_type_query:
        photos = photos.filter(photoType=photo_type_query)

    return render(request, 'core/home.html', {'photo_uploads': photos})
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

@login_required
def uploadPhotoPageView(request):
    if request.method == 'POST':
        form = fotoForm(request.POST, request.FILES)
        if form.is_valid():
            foto = form.save(commit=False)
            foto.name = request.user.get_full_name()  # Utilizar el nombre completo del usuario
            foto.place = f"{request.POST.get('latitude')}, {request.POST.get('longitude')}"
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            print("Latitude:", latitude, "Longitude:", longitude)  # Añadir para depuración
            foto.place = f"{latitude}, {longitude}"
            foto.save()
            return redirect('home')
    else:
        form = fotoForm()
    
    return render(request, 'photo/uploadphoto.html', {'form': form})
