from django.urls import path
from . import views

urlpatterns = [
    path("registro/", views.registro, name="registro"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("projetos/", views.projetos, name="projetos"),
    path("projetos/<int:projeto_id>/tarefas/", views.tarefas_por_projeto, name="tarefas_por_projeto"),
    path('perfil/', views.perfil, name='perfil'),
    path('tarefa/editar/<int:tarefa_id>/', views.editar_tarefa, name='editar_tarefa'),
    path('projetos/delete/<int:projeto_id>/', views.delete_projeto, name='delete_projeto'),
    path('tarefa/<int:tarefa_id>/apontamentos/', views.apontamentos_tarefa, name='apontamentos_tarefa'),
]