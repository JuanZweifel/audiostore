from django.contrib import admin
from django.urls import include,path
from .views import index, categoria

urlpatterns = [
    path('', index, name='index'),
    path('categoria', categoria, name='categoria'),
]