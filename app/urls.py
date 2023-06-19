from django.contrib import admin
from django.urls import include,path
from .views import index, categoria, detalle_producto, index_admin

urlpatterns = [
    path('', index, name='index'),
    path('categoria', categoria, name='categoria'),
    path('producto/<int:id>/', detalle_producto, name='detalle_producto'),
    path('index_admin', index_admin, name='index_admin')
]