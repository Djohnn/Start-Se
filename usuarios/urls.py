from django.urls import path
from . import views

urlpatterns = [
    path('', views.cadastro, name="cadastro"),
    path('login/', views.login, name="login"),
    path('sair/', views.logout, name='logout')
]
