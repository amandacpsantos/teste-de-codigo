from django.urls import path, include
from .views import registrar_empresa, registrar_candidato, editar_candidato
urlpatterns = [

    path('Empresa/', registrar_empresa, name='regEmpresa'),
    path('Candidato/', registrar_candidato, name='regCandidato'),
    path('editar_candidato/', editar_candidato, name='editar_candidato'),

]