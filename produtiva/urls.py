from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("registro/", views.registro, name="registro"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("projetos/", views.projetos, name="projetos"),
    path("projetos/<int:projeto_id>/tarefas/", views.tarefas_por_projeto, name="tarefas_por_projeto"),
    path('perfil/', views.perfil, name='perfil'),
    path('tarefa/editar/<int:tarefa_id>/', views.editar_tarefa, name='editar_tarefa'),
    path('tarefa/<int:tarefa_id>/apontamentos/', views.apontamentos_tarefa, name='apontamentos_tarefa'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"), name="password_reset"),       
    path('reset_password/sent/', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset_password/complete/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name="password_reset_complete"),
    path("projetos/delete/<int:projeto_id>/", views.excluir_definitivamente, name="delete_projeto"),
    path('projetos/cancelar/<int:projeto_id>/', views.cancelar_projeto, name='cancelar_projeto'),
    path('projetos/restaurar/<int:projeto_id>/', views.restaurar_projeto, name='restaurar_projeto'),
    path('projetos/excluir_definitivamente/<int:projeto_id>/', views.excluir_definitivamente, name='excluir_definitivamente'),

]