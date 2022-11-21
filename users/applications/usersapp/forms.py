from dataclasses import fields
from re import T
from django import forms
from django.contrib.auth import authenticate
from .models import User


class UserRegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Conrtaseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Constraseña'
            }
        )
    )
    password2 = forms.CharField(
        label='Conrtaseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Repetir constraseña'
            }
        )
    )

    class Meta:

        model= User
        fields= (

            'username',
            'names',
            'last_name',
            'email',
            'gender',
        )
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'las contraseñas no son iguales')

class LoginForm(forms.Form):

    username= forms.CharField(
        label= 'Usuario',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Usuario',
                'style' : '{margin: 10px}',
                
            }
        )
    )
    password = forms.CharField(
        label='Conrtaseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Constraseña'
            }
        )
    )
    #Validacion de los datos ingresados en login
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate( username=username, password=password):
            raise forms.ValidationError('Usuario o Contraseña incorrectos')

        return self.cleaned_data

class UpdatePasswordForm(forms.Form):

    password1 = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Constraseña Actual'
            }
        )
    )
    password2 = forms.CharField(
        label='New Password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Constraseña Nueva'
            }
        )
    )

class VarificationForm(forms.Form):
    codregistro = forms.CharField(required=True, label= 'Codigo')

    def __init__(self, pk, *args, **kwargs):

        self.id_user =pk
        super(VarificationForm, self).__init__(*args, **kwargs)



    def clean_codregistro(self):
        codigo = self.cleaned_data['codregistro']

        if len(codigo) ==6:
            #verificacoines si el codigo y el id son validaos
            activo =User.objects.cod_validation(
                self.id_user,
                codigo
            )
            if not activo:
                raise forms.ValidationError('Usuario o Contraseña incorrectos')   
        else:
            raise forms.ValidationError('Usuario o Contraseña incorrectos')