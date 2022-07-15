from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Venta

class VentaForm(forms.ModelForm):

    class Meta:
        model = Venta
        fields = '__all__'





class usuarioRegistro(UserCreationForm):    
    
    class Meta:
        model= User
        fields = ['username','first_name','last_name',"email",'password1','password2']


class usuarioEdit(UserCreationForm):    
    
    class Meta:
        model= User
        fields = ['username','first_name','last_name',"email","is_staff"]

class usuarioAdmin(UserCreationForm):    
    
    class Meta:
        model= User
        fields = ['username','first_name','last_name',"email","is_staff"]
