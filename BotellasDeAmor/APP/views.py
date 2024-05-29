from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.http import HttpResponse
from django import forms
from django.urls import reverse
from openpyxl import Workbook
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
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    punto_acopio_query = request.GET.get('punto_acopio')
    consecutive_number_query = request.GET.get('consecutive_number')
    material_type_query = request.GET.get('materialType')  # Nuevo filtro


    photos = Foto.objects.all()

    if filter_option == 'recent':
        photos = photos.order_by('-date')
    elif filter_option == 'oldest':
        photos = photos.order_by('date')

    if name_query:
        photos = photos.filter(name__icontains=name_query)

    if photo_type_query:
        photos = photos.filter(photoType=photo_type_query)

    if date_from and date_to:
        date_from_obj = datetime.datetime.strptime(date_from, '%Y-%m-%d')
        date_to_obj = datetime.datetime.strptime(date_to, '%Y-%m-%d')
        photos = photos.filter(date__range=[date_from_obj, date_to_obj])

    if punto_acopio_query:
        photos = photos.filter(punto_acopio__icontains=punto_acopio_query)
        
    if consecutive_number_query:
        photos = photos.filter(merchandise__consecutive_number=consecutive_number_query)
        
    if material_type_query:
        photos = photos.filter(material_type=material_type_query)  # Aplicar el filtro


    # Agrupar las fotos por número de consecutivo
    grouped_photos = {}
    for photo in photos:
        key = photo.merchandise.consecutive_number
        if key not in grouped_photos:
            grouped_photos[key] = []
        grouped_photos[key].append(photo)

    return render(request, 'core/home.html', {'grouped_photos': grouped_photos})

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
        form = FotoForm(request.POST, request.FILES)
        if form.is_valid():
            consecutive_number = form.cleaned_data['consecutive_number']
            weight = form.cleaned_data['weight'] or 0
            merchandise, created = Merchandise.objects.get_or_create(
                consecutive_number=consecutive_number
            )
            if not created and weight:
                merchandise.weight += weight
                merchandise.save()
            elif created:
                merchandise.weight = weight
                merchandise.save()

            foto = form.save(commit=False)
            foto.merchandise = merchandise
            foto.name = request.user.get_full_name()
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            foto.place = f"{latitude}, {longitude}"
            foto.save()
            return redirect('home')
    else:
        form = FotoForm()

    return render(request, 'photo/uploadphoto.html', {'form': form})


@login_required
def download_excel_report(request):
    filter_option = request.GET.get('filter')
    name_query = request.GET.get('name')
    photo_type_query = request.GET.get('photoType')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    material_type_query = request.GET.get('materialType')

    photos = Foto.objects.all()

    if filter_option == 'recent':
        photos = photos.order_by('-date')
    elif filter_option == 'oldest':
        photos = photos.order_by('date')

    if name_query:
        photos = photos.filter(name__icontains=name_query)

    if photo_type_query:
        photos = photos.filter(photoType=photo_type_query)

    if date_from and date_to:
        date_from_obj = datetime.datetime.strptime(date_from, '%Y-%m-%d')
        date_to_obj = datetime.datetime.strptime(date_to, '%Y-%m-%d')
        photos = photos.filter(date__range=[date_from_obj, date_to_obj])

    if material_type_query:
        photos = photos.filter(material_type=material_type_query)

    # Crear un libro de Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte de Fotos"

    # Encabezados
    headers = ['Name', 'Photo Type', 'Date', 'Place', 'Material Type', 'Consecutive Number', 'Weight']
    ws.append(headers)

    # Agregar datos
    for photo in photos:
        ws.append([
            photo.merchandise.consecutive_number,
            photo.name,
            photo.get_photoType_display(),
            photo.date.strftime('%Y-%m-%d %H:%M:%S'),
            photo.place,
            photo.get_material_type_display(),
            photo.weight
        ])

    # Preparar la respuesta HTTP con el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=reporte_fotos.xlsx'
    wb.save(response)
    return response