from .models import Candidato, Empresa
from django.contrib.auth.forms import UserCreationForm
from django import forms

class EmpresaForm(UserCreationForm):
    class Meta:
        model = Empresa
        fields = ['first_name', 'email',]

class CandidatoForm(UserCreationForm):
    class Meta:
        model = Candidato
        fields = ['first_name', 'email',]

class UserFormUp(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class ExperienciaForm(forms.Form):
    """
    Form para experiencias do candidato
    """




    anchor = forms.CharField(
                    max_length=100,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Link Name / Anchor Text',
                    }),
                    required=False)
    url = forms.URLField(
                    widget=forms.URLInput(attrs={
                        'placeholder': 'URL',
                    }),
                    required=False)