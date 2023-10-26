from django.urls import path
from equipamentos import views

urlpatterns = [
    path('equipamentos/', views.lista_equipamentos, name='lista_equipamentos'),
    path('equipamentos/adicionar/', views.adicionar_equipamento, name='adicionar_equipamento'),
]
