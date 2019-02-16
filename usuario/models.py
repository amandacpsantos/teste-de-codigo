from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    categoria = models.PositiveIntegerField(default=0)
    username = models.CharField(max_length=10, unique=False, blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True)
    is_staff = models.BooleanField(default=True, )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['EMAIL_FIELD']

    def get_categoria(self):
        return self.categoria


class Empresa(User):
    nome = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'


class Experiencia(models.Model):
    empresa = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50)
    inicio = models.DateField(null=True, blank=True, verbose_name='início')
    final = models.DateField(null=True, blank=True, verbose_name='final')
    resumo = models.TextField(max_length=500)


class Candidato(User):

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

    pretensao_salarial = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,)
    ultima_escolaridade = models.CharField(
        max_length=50,
        choices=ESCOLARIDADE,
        default=EF,
        null=True,
        blank=True,
    )

    experiencias = models.ManyToManyField(Experiencia)

    class Meta:
        verbose_name = 'Candidato'
        verbose_name_plural = 'Candidatos'

