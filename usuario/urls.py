from django.urls import path
from .views import registrar_empresa, registrar_candidato, editar_candidato, editar_empresa

urlpatterns = [

    path('Empresa/', registrar_empresa, name='regEmpresa'),
    path('Candidato/', registrar_candidato, name='regCandidato'),
    path('editar_candidato/', editar_candidato, name='editar_candidato'),
    path('editar_empresa/', editar_empresa, name='editar_empresa'),

]