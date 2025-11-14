from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from produtiva.models import Apontamento, Tarefa, Projeto
from django.utils import timezone

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
        
        if User.objects.filter(username=email).exists():
            messages.error(
                request,
                "Este e-mail já está cadastrado.",
                extra_tags="email_error",
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
        if request.GET.get('next'):
            messages.warning(request, "Você precisa estar logado para acessar essa página.")
            
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
            
            
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url) 
            
            return redirect("/produtiva/projetos/")

        messages.add_message(request, constants.ERROR, "E-mail ou senha inválidos.")
        return render(request, "login.html", {"data": {"login": email}})
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def logout(request):
    auth.logout(request)
    messages.add_message(request, constants.INFO, "Você foi desconectado.")
    return redirect("login")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
@login_required
def projetos(request):
    user = request.user

    if hasattr(user, 'perfil') and user.perfil.is_admin:
        projetos_do_usuario = Projeto.objects.all()
    else:
        projetos_do_usuario = Projeto.objects.filter(participantes=user)

    projetos_ativos = projetos_do_usuario.filter(cancelado=False, concluido=False)
    projetos_cancelados = projetos_do_usuario.filter(cancelado=True)
    projetos_concluidos = projetos_do_usuario.filter(concluido=True)

    if request.method == "POST" and user.perfil.is_admin:
        nome = request.POST.get("nome_projeto")
        descricao = request.POST.get("descricao")
        participantes_ids = request.POST.getlist("participantes")

        projeto = Projeto.objects.create(
            nome_projeto=nome,
            descricao=descricao,
            usuario=user
        )
        if participantes_ids:
            projeto.participantes.set(participantes_ids)

        messages.success(request, "Projeto criado com sucesso!")
        return redirect("projetos")

    context = {
        "projetos": projetos_ativos,
        "cancelados": projetos_cancelados,
        "concluidos": projetos_concluidos,
        "users": User.objects.all(),
    }

    return render(request, "projetos.html", context)

@login_required
def cancelar_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    if not request.user.perfil.is_admin:
        messages.error(request, "Apenas administradores podem cancelar projetos.")
        return redirect('projetos')
        
    projeto.cancelado = True
    projeto.save()
    messages.info(request, f'Projeto "{projeto.nome_projeto}" foi movido para cancelados.')
    return redirect('projetos')

@login_required
def concluir_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    
    if not request.user.perfil.is_admin:
        messages.error(request, "Apenas administradores podem concluir projetos.")
        return redirect('projetos')

    projeto.concluido = True
    projeto.cancelado = False 
    projeto.save()

    messages.success(request, f'Projeto "{projeto.nome_projeto}" foi concluído com sucesso!')
    return redirect('projetos')


@login_required
def restaurar_projeto_concluido(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    if not request.user.perfil.is_admin:
        messages.error(request, "Apenas administradores podem reabrir projetos concluídos.")
        return redirect('projetos')

    projeto.concluido = False
    projeto.save()
    messages.success(request, f'Projeto "{projeto.nome_projeto}" foi reaberto com sucesso!')
    return redirect('projetos')

@login_required
def restaurar_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    projeto.cancelado = False
    projeto.save()
    messages.success(request, f'Projeto "{projeto.nome_projeto}" foi restaurado!')
    return redirect('projetos')

@login_required
def excluir_definitivamente(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    projeto.delete()
    messages.success(request, f'Projeto "{projeto.nome_projeto}" foi excluído permanentemente.')
    return redirect('projetos')

@login_required
def editar_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)

    if not request.user.perfil.is_admin:
        messages.error(request, "Apenas administradores podem editar projetos.")
        return redirect('projetos')

    if request.method == "POST":
        nome = request.POST.get("nome_projeto")
        descricao = request.POST.get("descricao")
        participantes_ids = request.POST.getlist("participantes")

        projeto.nome_projeto = nome
        projeto.descricao = descricao
        projeto.save()

        if participantes_ids:
            projeto.participantes.set(participantes_ids)
        else:
            projeto.participantes.clear()

        messages.success(request, f'O projeto "{projeto.nome_projeto}" foi atualizado com sucesso!')
        return redirect('projetos')

    context = {
        "projeto": projeto,
        "users": User.objects.all(),
    }
    return render(request, "editar_projeto.html", context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def tarefas_por_projeto(request, projeto_id):
    user = request.user
    projeto = get_object_or_404(Projeto, id=projeto_id)

    if not (hasattr(user, 'perfil') and user.perfil.is_admin) and user not in projeto.participantes.all():
        messages.error(request, "Você não tem permissão para acessar este projeto.")
        return redirect('projetos')

    if request.method == 'POST':
        tarefa_id = request.POST.get('tarefa_id')
        nome_tarefa = request.POST.get('nome_tarefa')
        descricao = request.POST.get('descricao')
        estimativa_horas = request.POST.get('estimativa_horas')
        categoria = request.POST.get('categoria')

        if not nome_tarefa or not estimativa_horas or not categoria:
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
            return redirect('tarefas_por_projeto', projeto_id=projeto.id)

        if tarefa_id:
            tarefa = get_object_or_404(Tarefa, id=tarefa_id, projeto=projeto)
            if not (user == tarefa.usuario or user.perfil.is_admin or user in projeto.participantes.all()):
                messages.error(request, "Você não tem permissão para editar esta tarefa.")
                return redirect('tarefas_por_projeto', projeto_id=projeto.id)

            tarefa.nome_tarefa = nome_tarefa
            tarefa.descricao = descricao
            tarefa.estimativa_horas = estimativa_horas
            tarefa.categoria = categoria
            tarefa.save()
            messages.success(request, 'Tarefa atualizada com sucesso!')
        else:
            Tarefa.objects.create(
                nome_tarefa=nome_tarefa,
                descricao=descricao,
                estimativa_horas=estimativa_horas,
                categoria=categoria,
                projeto=projeto,
                usuario=user
            )
            messages.success(request, 'Tarefa adicionada ao projeto com sucesso!')

        return redirect('tarefas_por_projeto', projeto_id=projeto.id)

    context = {
        'projeto': projeto,
        'tarefas': projeto.tarefas.filter(cancelada=False, concluida=False),
        'tarefas_concluidas': projeto.tarefas.filter(concluida=True),
        'tarefas_canceladas': projeto.tarefas.filter(cancelada=True),
    }
    return render(request, 'tarefas_por_projeto.html', context)


@login_required
def editar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    user = request.user

    if not (user.perfil.is_admin or user in tarefa.projeto.participantes.all()):
        messages.error(request, "Você não tem permissão para editar esta tarefa.")
        return redirect('tarefas_por_projeto', projeto_id=tarefa.projeto.id)

    if request.method == "POST":
        tarefa.nome_tarefa = request.POST.get("nome_tarefa")
        tarefa.descricao = request.POST.get("descricao")
        tarefa.estimativa_horas = request.POST.get("estimativa_horas")
        tarefa.categoria = request.POST.get("categoria")
        tarefa.save()
        messages.success(request, "Tarefa atualizada com sucesso!")
        return redirect('tarefas_por_projeto', projeto_id=tarefa.projeto.id)

    context = {'tarefa': tarefa, 'projeto': tarefa.projeto}
    return render(request, 'editar_tarefa.html', context)


@login_required
def concluir_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    user = request.user

    if not (user.perfil.is_admin or user in tarefa.projeto.participantes.all()):
        messages.error(request, "Você não tem permissão para concluir esta tarefa.")
        return redirect('tarefas_por_projeto', projeto_id=tarefa.projeto.id)

    tarefa.concluida = True
    tarefa.cancelada = False
    tarefa.save()
    messages.success(request, f"Tarefa '{tarefa.nome_tarefa}' concluída com sucesso.")
    return redirect('tarefas_por_projeto', projeto_id=tarefa.projeto.id)


@login_required
def cancelar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    user = request.user

    if not (user.perfil.is_admin or user in tarefa.projeto.participantes.all()):
        messages.error(request, "Você não tem permissão para cancelar esta tarefa.")
        return redirect('tarefas_por_projeto', projeto_id=tarefa.projeto.id)

    tarefa.cancelada = True
    tarefa.concluida = False
    tarefa.save()
    messages.info(request, f"Tarefa '{tarefa.nome_tarefa}' foi cancelada.")
    return redirect('tarefas_por_projeto', projeto_id=tarefa.projeto.id)


@login_required
def restaurar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    user = request.user

    if not (user.perfil.is_admin or user in tarefa.projeto.participantes.all()):
        messages.error(request, "Você não tem permissão para restaurar esta tarefa.")
        return redirect('tarefas_por_projeto', projeto_id=tarefa.projeto.id)

    tarefa.cancelada = False
    tarefa.concluida = False
    tarefa.save()
    messages.success(request, f"Tarefa '{tarefa.nome_tarefa}' foi restaurada com sucesso.")
    return redirect('tarefas_por_projeto', projeto_id=tarefa.projeto.id)


@login_required
def excluir_tarefa_definitivo(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    user = request.user

    if not user.perfil.is_admin:
        messages.error(request, "Apenas administradores podem excluir tarefas permanentemente.")
        return redirect('tarefas_por_projeto', projeto_id=tarefa.projeto.id)

    tarefa.delete()
    messages.success(request, f"Tarefa '{tarefa.nome_tarefa}' excluída permanentemente.")
    return redirect('tarefas_por_projeto', projeto_id=tarefa.projeto.id)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def perfil(request):
    user = request.user
    perfil = user.perfil  # relação 1-1

    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exclude(pk=user.pk).exists():
            messages.error(request, 'Este e-mail já está em uso por outro utilizador.')
            password_form = PasswordChangeForm(user, request.POST)
            context = {'password_form': password_form, 'user': user, 'perfil': perfil}
            return render(request, 'perfil.html', context)

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = email
        user.save()

        # Foto de perfil
        if 'foto' in request.FILES:
            perfil.foto = request.FILES['foto']
            perfil.save()

        password_form = PasswordChangeForm(user, request.POST)
        old_password = request.POST.get('old_password')

        if old_password:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Perfil e senha atualizados com sucesso!')
                return redirect('perfil')
            else:
                messages.error(request, 'Não foi possível alterar a sua senha. Verifique os erros abaixo.')
        else:
            messages.success(request, 'As suas informações de perfil foram salvas!')

        return redirect('perfil')

    else:
        password_form = PasswordChangeForm(user)

    context = {'password_form': password_form, 'user': user, 'perfil': perfil}
    return render(request, 'perfil.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def apontamentos_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'start':
            if not tarefa.apontamento_ativo:
                Apontamento.objects.create(
                    tarefa=tarefa,
                    usuario=request.user,
                    hora_inicial=timezone.now()
                )
                messages.success(request, 'Apontamento iniciado!')
            else:
                messages.error(request, 'Esta tarefa já possui um apontamento em andamento.')

        elif action == 'stop':
            apontamento_id = request.POST.get('apontamento_id')
            descricao = request.POST.get('descricao')  

            try:
                apontamento_ativo = Apontamento.objects.get(
                    id=apontamento_id, 
                    tarefa=tarefa, 
                    hora_final__isnull=True
                )
                apontamento_ativo.hora_final = timezone.now()
                apontamento_ativo.descricao = descricao  
                apontamento_ativo.save()
                messages.success(request, 'Apontamento finalizado com sucesso!')
            except Apontamento.DoesNotExist:
                messages.error(request, 'Apontamento ativo não encontrado.')
        
        return redirect('apontamentos_tarefa', tarefa_id=tarefa.id)

    apontamentos_concluidos = Apontamento.objects.filter(
        tarefa=tarefa, 
        hora_final__isnull=False
    ).order_by('-hora_inicial')
    
    apontamento_ativo = tarefa.apontamento_ativo

    context = {
        'tarefa': tarefa,
        'apontamentos_concluidos': apontamentos_concluidos,
        'apontamento_ativo': apontamento_ativo
    }
    return render(request, 'apontamentos.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def relatorio_produtividade(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    tarefas = Tarefa.objects.filter(projeto=projeto)

    dados_tarefas = []
    total_estimado = 0.0
    total_gasto = 0.0

    for t in tarefas:
        if t.cancelada:
            dados_tarefas.append({
                "nome": t.nome_tarefa,
                "status": "Cancelada",
                "estimado": "-",
                "gasto": "-",
                "diferenca": "-",
            })
            continue

        if not t.concluida:
            continue

        estimado_horas = (
            t.estimativa_horas.hour + t.estimativa_horas.minute / 60
            if t.estimativa_horas else 0
        )

        gasto_horas = 0
        if t.total_horas_gastas_str:
            try:
                h, m = map(int, t.total_horas_gastas_str.split(":"))
                gasto_horas = h + m / 60
            except ValueError:
                gasto_horas = 0

        if gasto_horas == 0:
            dados_tarefas.append({
                "nome": t.nome_tarefa,
                "status": "Não executada",
                "estimado": round(estimado_horas, 2),
                "gasto": 0,
                "diferenca": "-",
            })
            continue

        total_estimado += estimado_horas
        total_gasto += gasto_horas

        dados_tarefas.append({
            "nome": t.nome_tarefa,
            "status": "Concluída",
            "estimado": round(estimado_horas, 2),
            "gasto": round(gasto_horas, 2),
            "diferenca": round(gasto_horas - estimado_horas, 2),
        })

    diferenca_total = round(total_gasto - total_estimado, 2)
    produtividade_percentual = 0
    if total_estimado > 0:
        produtividade_percentual = round(
            (min(total_estimado, total_gasto) / total_estimado) * 100, 1
        )

    contexto = {
        "projeto": projeto,
        "tarefas": dados_tarefas,
        "total_estimado": round(total_estimado, 2),
        "total_gasto": round(total_gasto, 2),
        "diferenca_total": diferenca_total,
        "produtividade_percentual": produtividade_percentual,
    }

    return render(request, "relatorio_produtividade.html", contexto)

def csrf_error_view(request, reason=""):
    """Exibe página amigável de erro CSRF"""
    return render(request, '403.html', status=403)