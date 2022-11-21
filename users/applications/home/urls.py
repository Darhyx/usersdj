from django.contrib import admin
from django.urls import path, re_path, include
from .views import HomePage, TemplatePruebaMixin

app_name= 'home_app'

urlpatterns = [
    path('index/', HomePage.as_view(), name= 'home' ),
    path('mixin/', TemplatePruebaMixin.as_view(), name= 'mixin' )
    
]