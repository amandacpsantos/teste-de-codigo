import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import VagaForm
from .models import Vaga, Aplicacao, Candidato, Empresa
from usuario.models import Experiencia
from django.contrib import messages

from django.db.models import Count
from django.db.models.functions import TruncMonth


@login_required
def dashboard(request):
    grupo_datas = Vaga.objects.annotate(month=TruncMonth('data')).values('month').annotate(
        total=Count('nome')).order_by('month')
    grupo_candidatos = Aplicacao.objects.annotate(month=TruncMonth('data')).values('month').annotate(
        total=Count('candidato')).order_by('month')

    datas_vagas = []
    total_vagas = []

    datas_candidatos = []
    total_candidatos = []

    for data in grupo_datas:
        datas_vagas.append('{}/{}'.format(data['month'].month, data['month'].year))
        total_vagas.append(data['total'])

    for candidato in grupo_candidatos:
        datas_candidatos.append('{}/{}'.format(candidato['month'].month, candidato['month'].year))
        total_candidatos.append(candidato['total'])

    if len(datas_vagas) > 12:
        datas_vagas = datas_vagas[-12]
        total_vagas = total_vagas[-12]

    if len(datas_candidatos) > 12:
        datas_candidatos = datas_candidatos[-12]
        total_candidatos = total_candidatos[-12]

    context = {
        'datas_vagas': json.dumps(datas_vagas),
        'total_vagas': json.dumps(total_vagas),
        'datas_candidatos': json.dumps(datas_candidatos),
        'total_candidatos': json.dumps(total_candidatos),
    }
    return render(request, 'dashboard.html', context)


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
    Listar todas as vagas cadastradas e disponíveis para visualização.
    :param request: Request.
    :return: Dicionário com dados de todas as vagas.
    """
    vagas = Vaga.objects.all().filter(delete=False)
    return render(request, "listar_vagas.html", {'vagas': vagas})


@login_required
def aplicar_vaga(request, id_vaga):
    """
    Busca os dados da vaga e altera o atributo 'delete' para True.
    :param request: Request.
    :param id_vaga: número de identificador da vaga.
    :return: Redirecionamento para tela de vagas.
    """

    # verifica se já existe entre os elementos da vaga
    vaga = get_object_or_404(Vaga, pk=id_vaga)
    result = vaga.aplicacoes.filter(candidato=request.user)

    if result.exists() == False:
        candidato = get_object_or_404(Candidato, user_ptr_id=request.user.id)
        vaga.aplicacoes.create(candidato=candidato)
        messages.success(request, 'Boa sorte!')
    else:
        messages.info(request, 'Você já está cadastrado!')

    return redirect('listar_vagas')


@login_required
def deletar_vaga(request, id_vaga):
    """
    Busca os dados da vaga e altera o atributo 'delete' para True.
    :param request: Request.
    :param id_vaga: número de identificador da vaga.
    :return: Redirecionamento para tela de vagas.
    """
    Vaga.objects.filter(pk=id_vaga).update(delete=True)
    return redirect('minhas_vagas')


@login_required
def alterar_vaga(request, id_vaga):
    """
    Busca os dados da vaga e persiste as alterações.
    :param request: Request.
    :param id_vaga: número de identificador da vaga.
    :return: Redirecionamento para tela de vagas ou dicionário contendo dados e campos do formulário
    """
    vaga = get_object_or_404(Vaga, pk=id_vaga)
    form = VagaForm(request.POST or None, instance=vaga)

    if form.is_valid():
        form.save()
        return redirect('minhas_vagas')
    else:
        return render(request, 'editar_vaga.html', {'form': form})


@login_required
def minhas_vagas(request):
    # (1, Empresa)
    # (0, Candidato)
    if request.user.categoria == 1:
        vagas = Vaga.objects.all().filter(delete=False, empresa=request.user)
        return render(request, "minhas_vagas.html", {'vagas': vagas})
    else:
        vagas = Vaga.objects.filter(delete=False, aplicacoes__candidato=request.user).distinct()
        return render(request, "vagas_aplicadas.html", {'vagas': vagas})


@login_required
def detalhes_vaga(request, id_vaga):
    faixa = {'Até 1.000': 1000,
             'De 1.000 a 2.000': 2000,
             'De 2.000 a 3.000': 3000,
             'Acima de 3.000': 3001, }

    escolaridade = ['Ensino Fundamental', 'Ensino Médio', 'Tecnólogo', 'Ensino Superior', 'Pós / MBA / Mestrado',
                    'Doutorado']

    # busca os dados da vaga
    vaga = Vaga.objects.get(id=id_vaga)

    # busca todas as aplicações da vaga
    aplicacoes_vaga = vaga.aplicacoes.all()

    detalhes = []

    # busca as experiências de cada candidato e calcula a pontuação de acordo com escolaridade e pretensão salarial
    for aplicacao in aplicacoes_vaga:
        pontos = 0

        if aplicacao.candidato.ultima_escolaridade is not None and \
                (escolaridade.index(aplicacao.candidato.ultima_escolaridade) >= escolaridade.index(vaga.escolaridade)):
            pontos += 1

        if vaga.faixa_salarial in faixa:
            if aplicacao.candidato.pretensao_salarial - faixa[vaga.faixa_salarial] <= 0:
                pontos += 1

        exp = Experiencia.objects.filter(candidato=aplicacao.candidato)
        detalhes.append([aplicacao.candidato, exp, pontos])

    contexto = {'detalhes': detalhes, 'vaga': vaga}
    return render(request, "detalhes_vaga.html", contexto)
