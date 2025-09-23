from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from usuarios.models import Tarefa
from usuarios.models import Projeto


def registro(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        sobrenome = request.POST.get("sobrenome")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        confirmar_senha = request.POST.get("confirmar_senha")

        data = {
            "nome": nome,
            "email": email,
        }

        has_error = False

        if not nome and not sobrenome:
            messages.error(request, "Campo Obrigatório", extra_tags="nome_error")
            has_error = True

        if not email:
            messages.error(request, "Campo Obrigatório", extra_tags="email_error")
            has_error = True

        if not senha and not confirmar_senha:
            messages.error(request, "Campo Obrigatório", extra_tags="senha_error")
            has_error = True
        elif len(senha) > 1 and len(senha) < 6:
            messages.error(
                request,
                "A senha deve conter pelo menos 6 caracteres",
                extra_tags="senha_error",
            )
            has_error = True

        if senha != confirmar_senha:
            messages.error(
                request, "As senhas não coincidem", extra_tags="confirmar_senha_error"
            )
            has_error = True

        if has_error:
            return render(request, "registro.html", {"data": data})

        user = User.objects.create_user(
            username=email,
            email=email,
            password=senha,
            first_name=nome,
            last_name=sobrenome,
        )
        user.save()

        messages.success(request, "Usuário cadastrado com sucesso!")
        return redirect("login")

    return render(request, "registro.html")


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        user = authenticate(request, username=email, password=senha)

        if user:
            auth.login(request, user)
            messages.add_message(
                request, constants.SUCCESS, f"Bem-vindo, {user.first_name}!"
            )
            return redirect("/usuarios/projetos/")

        messages.add_message(request, constants.ERROR, "E-mail ou senha inválidos.")
        return render(request, "login.html", {"data": {"login": email}})


@login_required
def logout(request):
    auth.logout(request)
    messages.add_message(request, constants.INFO, "Você foi desconectado.")
    return redirect("login")


@login_required
def logout(request):
    return redirect("projetos.html")


@login_required
def projetos(request):
    projetos = Projeto.objects.filter(usuario=request.user).order_by("-data_criacao")
    return render(request, "projetos.html", {"projetos": projetos})


@login_required
def lista_tarefas(request):
    tarefas = Tarefa.objects.filter(usuario=request.user).order_by('nome_tarefa')

    if request.method == 'POST':
        try:
            nome_tarefa = request.POST.get('nome_tarefa')
            descricao = request.POST.get('descricao')
            estimativa_horas = request.POST.get('estimativa_horas') 
            categoria = request.POST.get('categoria')
            projeto_padrao, created = Projeto.objects.get_or_create(
                nome_projeto="Projeto padrão",
                usuario=request.user
            )

            Tarefa.objects.create(
                nome_tarefa=nome_tarefa,
                descricao=descricao,
                estimativa_horas=estimativa_horas, 
                categoria=categoria,
                projeto=projeto_padrao,
                usuario=request.user
            )
            
            messages.success(request, 'Tarefa criada com sucesso!')
            return redirect('listatarefas')

        except Exception as e:
            messages.error(request, f"Erro ao criar a tarefa: {e}")
            print(f"Erro: {e}")

    return render(request, "listaTarefas.html", {
        "tarefas": tarefas,
    })
