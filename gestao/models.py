from django.db import models
from django.contrib.auth.models import AbstractUser
from .enums import FaixaSalarial, Escolaridade


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['USERNAME_FIELD']


class Vaga(models.Model):
    nome = models.CharField(max_length=50),
    faixa_salarial = models.CharField(
        max_length=5,
        choices=[(tag, tag.value) for tag in FaixaSalarial]),
    requisitos = models.TextField(max_length=500),
    escolaridade = models.CharField(
        max_length=5,
        choices=[(tag, tag.value) for tag in Escolaridade]),

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = 'Vagas'


class Candidato(User):
    pretensao_salarial = models.DecimalField(max_digits=10, decimal_places=2)
    ultima_escolaridade = models.CharField(
        max_length=5,
        choices=[(tag, tag.value) for tag in Escolaridade]),


class Experiencia(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, verbose_name='candidato')
    empresa = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50)
    inicio = models.DateField(null=True, blank=True, verbose_name='início')
    final = models.DateField(null=True, blank=True, verbose_name='final')
    resumo = models.TextField(max_length=500)




