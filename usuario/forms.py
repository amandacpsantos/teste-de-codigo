from .models import Candidato, Empresa, Experiencia
from django.contrib.auth.forms import UserCreationForm
from django import forms


class EmpresaForm(UserCreationForm):
    class Meta:
        model = Empresa
        fields = ['first_name', 'email', ]


class CandidatoForm(UserCreationForm):
    class Meta:
        model = Candidato
        fields = ['first_name', 'email', ]


class CandidatoEditForm(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = ['first_name', 'last_name', 'email', 'pretensao_salarial', 'ultima_escolaridade']


class ExperienciaForm(forms.ModelForm):
    class Meta:
        model = Experiencia
        fields = ['candidato', 'empresa', 'cargo', 'inicio', 'final', 'resumo']


#ExperienciaFormSet = forms.inlineformset_factory(Candidato, Experiencia, form=ExperienciaForm, extra=1)


