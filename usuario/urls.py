from django.urls import path, include
from .views import registrar_empresa, registrar_candidato

urlpatterns = [

    path('Empresa/', registrar_empresa, name='regEmpresa'),
    path('Candidato/', registrar_candidato, name='regCandidato'),

]