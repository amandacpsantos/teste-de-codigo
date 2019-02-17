from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from .models import Candidato, Empresa, Experiencia
from .forms import CandidatoEditForm, ExperienciaForm, EmpresaEditForm


from .models import User, Experiencia
from .forms import CandidatoForm, EmpresaForm, CandidatoEditForm
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


@csrf_protect
def registrar_empresa(request):
    form = EmpresaForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            empresa = form.save(commit=False)
            empresa.categoria = 1
            empresa.save()
            return redirect('login')

    return render(request, 'register.html', {'form': form})


@login_required
@csrf_protect
def editar_candidato(request):
    candidato = get_object_or_404(Candidato, user_ptr_id=request.user.id)
    ExperienciaFormset = inlineformset_factory(Candidato, Experiencia, fields=('empresa', 'cargo',), extra=1, max_num=5)

    if request.method == "POST":
        experiencias = ExperienciaFormset(request.POST, instance=candidato)
        candidato = CandidatoEditForm(request.POST, instance=candidato)

        if experiencias.is_valid() and candidato.is_valid():
            candidato.save()
            experiencias.save()
            return redirect('dashboard')

    else:
        experiencias = ExperienciaFormset(instance=candidato)
        candidato = CandidatoEditForm(instance=candidato)

    return render(request, "candidato_form.html", {"exp": experiencias, "cad": candidato})


@login_required
def editar_empresa(request):
    empresa = get_object_or_404(Empresa, user_ptr_id=request.user.id)
    form = EmpresaEditForm(request.POST or None, instance=empresa)

    if form.is_valid():
        form.save()
        messages.success(request, 'Alteração com sucesso!')
        return redirect('editar_empresa')
    else:
        return render(request, 'empresa_form.html', {'form': form})