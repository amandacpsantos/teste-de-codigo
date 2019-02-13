from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Candidato, Vaga, Experiencia




admin.site.register(User, UserAdmin)