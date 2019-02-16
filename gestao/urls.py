from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.urls import path, include
from .views import dashboard, cadastrar_vaga, listar_vagas, deletar_vaga, alterar_vaga, aplicar_vaga, minhas_vagas, detalhes_vaga

urlpatterns = [

    # DASHBOARD
    path('', dashboard, name='dashboard'),

    # MENU URLS
    path('listar_vagas/', listar_vagas, name='listar_vagas'),
    path('minhas_vagas/', minhas_vagas, name='minhas_vagas'),

    # VAGAS URLS
    path('cadastrar_vaga/', cadastrar_vaga, name='cadastrar_vaga'),
    path('alterar_vaga/<int:id_vaga>', alterar_vaga, name='alterar_vaga'),
    path('deletar_vaga/<int:id_vaga>', deletar_vaga, name='deletar_vaga'),
    path('aplicar_vaga/<int:id_vaga>', aplicar_vaga, name='aplicar_vaga'),
    path('detalhes_vaga/<int:id_vaga>', detalhes_vaga, name='detalhes_vaga'),


]
