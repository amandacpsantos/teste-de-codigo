from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from .models import Candidato, Empresa, Experiencia
from .forms import CandidatoEditForm, ExperienciaForm, EmpresaEditForm
from .models import Experiencia
from .forms import CandidatoForm, EmpresaForm, CandidatoEditForm

from django.views.decorators.csrf import csrf_protect


@csrf_protect
def registrar_candidato(request):
    """
    Recebe os dados do candidato contido no formulário e persiste caso esteja válido.
    :param request: Requisição POST.
    :return:Redirecionamento para tela de login ou o dicionário com os campos do formulário.
    """
    form = CandidatoForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success()
            return redirect('login')

    return render(request, 'register.html', {'form': form})


@csrf_protect
def registrar_empresa(request):
    """
    Recebe os dados da empresa contido no formulário e persiste caso esteja válido.
    :param request: Requisição POST.
    :return:Redirecionamento para tela de login ou dicionários contendo campos do formulário.
    """
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
    """
    Busca os dados do usuário autenticado, relaciona com os dados de da tabela 'experiência' e persiste as alterações.
    :param request: Requisição POST.
    :return:Redirecionamento para tela de edição ou dois dicionários contendo dados do usuário e as experiências e
    campos dos formulários.
    """
    candidato = get_object_or_404(Candidato, user_ptr_id=request.user.id)
    ExperienciaFormset = inlineformset_factory(Candidato, Experiencia, fields=('empresa', 'cargo',), extra=1, max_num=3)

    if request.method == "POST":
        experiencias = ExperienciaFormset(request.POST, instance=candidato)
        candidato = CandidatoEditForm(request.POST, instance=candidato)

        if experiencias.is_valid() and candidato.is_valid():
            candidato.save()
            experiencias.save()
            messages.success(request, 'Alteração realizada com sucesso!')
            return redirect('editar_candidato')

    else:
        messages.info(request, 'Verifique seus dados!')
        experiencias = ExperienciaFormset(instance=candidato)
        candidato = CandidatoEditForm(instance=candidato)

    return render(request, "candidato_form.html", {"exp": experiencias, "cad": candidato})


@login_required
def editar_empresa(request):
    """
    Busca os dados do usuário autenticado e persiste as alterações.
    :param request: Requisição POST.
    :return:Redirecionamento para tela de edição ou dicionário contendo dados do usuário e campos do formulário.
    """
    empresa = get_object_or_404(Empresa, user_ptr_id=request.user.id)
    form = EmpresaEditForm(request.POST or None, instance=empresa)

    if form.is_valid():
        form.save()
        messages.success(request, 'Alteração com sucesso!')
        return redirect('editar_empresa')
    else:
        return render(request, 'empresa_form.html', {'form': form})