from django.db import IntegrityError
from django.http.response import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import VagaForm
from .models import Vaga, Aplicacao, Candidato, Empresa
from usuario.models import Experiencia
from django.contrib import messages


def dashboard(request):
    return render(request, "dashboard.html")


@login_required
def cadastrar_vaga(request):
    form = VagaForm(request.POST or None)
    if form.is_valid():
        vaga = form.save(commit=False)
        emp = get_object_or_404(Empresa, user_ptr_id=request.user.id)
        vaga.empresa = emp
        vaga.save()
        return redirect('listar_vagas')
    else:
        return render(request, 'cadastrar_vaga.html', {'form': form})


@login_required()
def listar_vagas(request):
    """
    :param request:
    :return: request.Response
    """
    vagas = Vaga.objects.all().filter(delete=False)
    return render(request, "listar_vagas.html", {'vagas': vagas})


@login_required
def aplicar_vaga(request, id_vaga):
    """
    :param request:
    :param id_vaga
    :return: HttpResponse
    """

    #verifica se já existe entre os elementos da vaga
    vaga = get_object_or_404(Vaga, pk=id_vaga)
    result = vaga.aplicacoes.filter(candidato=request.user)

    if result.exists() == False:
        candidato = get_object_or_404(Candidato, user_ptr_id=request.user.id)
        vaga.aplicacoes.create(candidato=candidato)
        messages.success(request, 'Boa sorte!')
    else:
        messages.info(request, 'Você já está cadastrado')

    return redirect('listar_vagas')


@login_required
def deletar_vaga(request, id_vaga):
    Vaga.objects.filter(pk=id_vaga).update(delete=True)
    return redirect('minhas_vagas')


@login_required
def alterar_vaga(request, id_vaga):
    vaga = get_object_or_404(Vaga, pk=id_vaga)
    form = VagaForm(request.POST or None, instance=vaga)

    if form.is_valid():
        form.save()
        return redirect('minhas_vagas')
    else:
        return render(request, 'editar_vaga.html', {'form': form})


def minhas_vagas(request):
    # (1, Empresa)
    # (0, Candidato)
    if request.user.categoria == 1:
        vagas = Vaga.objects.all().filter(delete=False, empresa=request.user)
        return render(request, "minhas_vagas.html", {'vagas': vagas})
    else:
        vagas = Vaga.objects.filter(delete=False, aplicacoes__candidato=request.user).distinct()
        return render(request, "minhas_vagas.html", {'vagas': vagas})


@login_required
def detalhes_vaga(request, id_vaga):
    # get vaga
    vaga = Vaga.objects.get(id=id_vaga)

    # get todas as aplicações da vaga
    aplicacoes_vaga = vaga.aplicacoes.all()

    detalhes = []

    for aplicacao in aplicacoes_vaga:
        exp = Experiencia.objects.filter(candidato=aplicacao.candidato)
        detalhes.append([aplicacao.candidato, exp])

    contexto = {'detalhes': detalhes, 'vaga': vaga}
    print(contexto)
    return render(request, "detalhes_vaga.html", contexto)
