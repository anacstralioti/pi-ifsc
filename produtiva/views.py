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
            
            # ADICIONE ISSO:
            # Pega o parâmetro 'next' que foi enviado pelo formulário
            # (Veja o Passo 3 sobre como adicionar isso no HTML)
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url) # Redireciona para a página original
            
            # Se não houver 'next', vai para a página padrão
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
def projetos(request):
    if request.method == 'POST':
        nome_recebido = request.POST.get('nome_projeto')
        descricao_recebida = request.POST.get('descricao', '')      

        if nome_recebido and nome_recebido.strip():
            try:
                Projeto.objects.create(
                    nome_projeto=nome_recebido,
                    descricao=descricao_recebida,
                    usuario=request.user
                )
                messages.success(request, 'Projeto criado com sucesso!')
            except Exception as e:
                messages.error(request, f'Ocorreu um erro no servidor: {e}')
        else:
            messages.error(request, 'O nome do projeto não pode estar em branco.')
        
        return redirect('projetos')

    projetos_do_usuario = Projeto.objects.filter(usuario=request.user).order_by("-data_criacao")
    return render(request, "projetos.html", {"projetos": projetos_do_usuario})

@login_required
def delete_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id, usuario=request.user)
    projeto.delete()
    messages.success(request, f'Projeto "{projeto.nome_projeto}" removido com sucesso!')
    return redirect('projetos')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def tarefas_por_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id, usuario=request.user)
    
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
            tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)
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
                usuario=request.user
            )
            messages.success(request, 'Tarefa adicionada ao projeto com sucesso!')

        return redirect('tarefas_por_projeto', projeto_id=projeto.id)

    tarefas = Tarefa.objects.filter(projeto=projeto).order_by('nome_tarefa')
    context = { 'projeto': projeto, 'tarefas': tarefas }
    return render(request, 'tarefas_por_projeto.html', context)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def editar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)

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


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def perfil(request):
    user = request.user

    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exclude(pk=user.pk).exists():
            messages.error(request, 'Este e-mail já está em uso por outro utilizador.')
            password_form = PasswordChangeForm(user, request.POST)
            context = {'password_form': password_form, 'user': user}
            return render(request, 'perfil.html', context)
        
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = email
        user.save()

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
                context = {'password_form': password_form, 'user': user}
                return render(request, 'perfil.html', context)
        else:
            messages.success(request, 'As suas informações de perfil foram salvas!')
            return redirect('perfil')

    else:
        password_form = PasswordChangeForm(user)

    context = {'password_form': password_form, 'user': user}
    return render(request, 'perfil.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def apontamentos_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)
    
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
            try:
                apontamento_ativo = Apontamento.objects.get(
                    id=apontamento_id, 
                    tarefa=tarefa, 
                    hora_final__isnull=True
                )
                apontamento_ativo.hora_final = timezone.now()
                apontamento_ativo.save()
                messages.success(request, 'Apontamento finalizado!')
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