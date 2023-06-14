from django.contrib import admin
from django.urls import include,path
from .views import index, categoria, detalle_producto

urlpatterns = [
    path('', index, name='index'),
    path('categoria', categoria, name='categoria'),
    path('producto/<int:id>/', detalle_producto, name='detalle_producto')
]