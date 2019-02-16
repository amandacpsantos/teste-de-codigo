from django.db import models
from usuario.models import Candidato, Empresa


class Aplicacao(models.Model):
    data = models.DateField(auto_now=True, editable=False)
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, verbose_name='candidato')


class Vaga(models.Model):
    A1 = 'Até 1.000'
    D1A2 = 'De 1.000 a 2.000'
    D2A3 = 'De 2.000 a 3.000'
    AC3 = 'Acima de 3.000'
    FAIXA_SALARIAL = (
        (A1, 'Até 1.000'),
        (D1A2, 'De 1.000 a 2.000'),
        (D2A3, 'De 2.000 a 3.000'),
        (AC3, 'Acima de 3.000'),
    )

    EF = 'Ensino Fundamental'
    EM = 'Ensino Médio'
    TG = 'Tecnólogo'
    ES = 'Ensino Superior'
    PS = 'Pós / MBA / Mestrado'
    DR = 'Doutorado'
    ESCOLARIDADE = (
        (EF, 'Ensino Fundamental'),
        (EM, 'Ensino Médio'),
        (TG, 'Tecnólogo'),
        (ES, 'Ensino Superior'),
        (PS, 'Pós / MBA / Mestrado'),
        (DR, 'Doutorado'),
    )

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name='empresa')

    nome = models.CharField(max_length=50, default='')

    faixa_salarial = models.CharField(
        max_length=50,
        choices=FAIXA_SALARIAL,
        default=A1,
    )

    escolaridade = models.CharField(
        max_length=50,
        choices=ESCOLARIDADE,
        default=EF,
    )

    requisitos = models.TextField(max_length=500, default='')
    delete = models.BooleanField(default=False, editable=False)
    aplicacoes = models.ManyToManyField(Aplicacao, editable=False, blank=True
                                        )

    def get_quantidade_aplicacoes(self):
        return self.aplicacoes.count()


    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = 'Vagas'




