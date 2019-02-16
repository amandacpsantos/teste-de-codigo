# Generated by Django 2.1.7 on 2019-02-16 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestao', '0012_auto_20190216_0548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aplicacao',
            name='candidato',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='candidato'),
        ),
        migrations.AlterField(
            model_name='vaga',
            name='aplicacoes',
            field=models.ManyToManyField(blank=True, editable=False, to='gestao.Aplicacao'),
        ),
    ]