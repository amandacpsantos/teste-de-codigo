from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.urls import path, include
from gestao import urls as gestao_urls
from usuario import urls as usuario_urls
from .forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), {'authentication_form': LoginForm}, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', auth_views.LoginView.as_view(), {'authentication_form': LoginForm}, name='login'),
    path('dashboard/', include(gestao_urls)),
    path('usuario/', include(usuario_urls)),

]
