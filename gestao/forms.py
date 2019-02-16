from django.forms import ModelForm, forms
from .models import Vaga

class VagaForm(ModelForm):
    class Meta:
        model = Vaga
        fields = '__all__'
        exclude = ['empresa',]
