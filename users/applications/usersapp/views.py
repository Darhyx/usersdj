from django.core.mail import send_mail
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, View
from django.views.generic.edit import FormView
from applications.usersapp.models import User
# Create your views here.
from .forms import (
UserRegisterForm, 
LoginForm, 
UpdatePasswordForm, 
VarificationForm)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from . import functions

class UserRegisterView(FormView):
    template_name = 'userapp/register.html'
    form_class=UserRegisterForm
    success_url='/'

    def form_valid(self, form):

        codigo = functions.code_generator()

        #funcion creada en los managers
        new_user= User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password1'],
                
                #extrafields

                    names=form.cleaned_data['names'],
                    last_name=form.cleaned_data['last_name'],
                    gender=form.cleaned_data['gender'],
                    codregistro= codigo
        )
        #enviar Codigo al correo del usuario

        asunto= 'Confirmacion de email'
        mensaje= f'Gracias por utilizar el sistema!!.\n Codigo de Verificacion: ' + codigo
        email_remitente= 'juandariomansilla@gmail.com'

        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'],])
        
        #redirigir a pantalla de validacion de codigo
        return HttpResponseRedirect(
            reverse(
                'users_app:user-verification',
                kwargs={'pk':new_user.id}
            )
        )


        


class LoginUser(FormView):
    template_name = 'userapp/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:home')

    def form_valid(self, form):
        #verificar si el usuario existe 
        user = authenticate(
           username= form.cleaned_data['username'],
           password=form.cleaned_data['password'],
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)

class LogoutView(View):

    def get(self, request, **Kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )

class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'userapp/update.html'
    form_class=UpdatePasswordForm
    success_url=reverse_lazy('users_app:user-login')
    login_url=reverse_lazy('users_app:user-login')

    def form_valid(self, form):
        usuario=self.request.user
        user = authenticate(
            username= usuario.username,
            password= form.cleaned_data['password1']        
        )
        # si la contraseña actual es correcta
        if user:
            new_password= form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()
            
        else:
            print('contrase actual incorrecta ')
        # FALTA ESTA PARTE
            #raise forms.ValidationError('error')
            form.add_error('password1','sdf')
        logout(self.request)

        return super(UpdatePasswordView, self).form_valid(form)


class CodeVerificationsView(FormView):
    template_name = 'userapp/verification.html'
    form_class = VarificationForm
    success_url= reverse_lazy('users_app:user-login')

    def get_form_kwargs(self):
        
        kwargs = super(CodeVerificationsView, self).get_form_kwargs()
        kwargs.update({

            'pk': self.kwargs['pk']

        })
        return kwargs 

    def form_valid(self, form):
        #
        User.objects.filter(

            id=self.kwargs['pk']
        ).update(
            is_active=True
        )
     

        return super(CodeVerificationsView, self).form_valid(form)