from django.contrib.auth import get_user
from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from .forms import CandidatoForm, EmpresaForm, UserFormUp
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_protect


@csrf_protect
def registrar_candidato(request):
    form = CandidatoForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'register.html', {'form': form})


def registrar_empresa(request):
    form = EmpresaForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            empresa = form.save(commit=False)
            empresa.categoria = 1
            empresa.save()
            return redirect('login')

    return render(request, 'register.html', {'form': form})