from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django import forms


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'password1', 'password2' ) 

    def clean_email(self):
        email=self.cleaned_data['email'].lower()
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f'Email {email} ya se encuentra en uso')
    
    def clean_name(self):
        name=self.cleaned_data['name'].lower()
        try:
            user = User.objects.get(name=name)
        except Exception as e:
            return name
        raise forms.ValidationError(f'El nombre {name} ya se encuentra en uso')
    



class FotoForm(forms.ModelForm):
    consecutive_number = forms.IntegerField(label='Número de Consecutivo', required=True)
    
    class Meta:
        model = Foto
        fields = ['image', 'photoType', 'weight', 'punto_acopio', 'material_type']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'photoType': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'punto_acopio': forms.TextInput(attrs={'class': 'form-control'}),
            'material_type': forms.Select(attrs={'class': 'form-control'}),
        }
