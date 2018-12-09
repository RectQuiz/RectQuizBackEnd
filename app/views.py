from datetime import date, datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
import json

ITEMS_PER_PAGE = 5

@login_required
def painel_geral(request, template_name="administracao/painel.html"):
    return render(request, template_name)

@login_required
def painel_estatistica(request, template_name="administracao/paineis/estatistica.html"):
    today = date.today()
    usuariosAtivos = User.objects.filter(is_staff=False).filter(last_login__gte=today)
    usuariosCadastrados = User.objects.filter(is_staff=False)
    denunciasAceitas = Denuncia.objects.filter(verificada="Aceita")
    denunciasRejeitadas = Denuncia.objects.filter(verificada="Rejeitada")
    denunciasEA = Denuncia.objects.filter(verificada="Em Análise")
    perguntas = Quiz.objects.all()
    temas = Quiz.objects.all()
    return render(request, template_name,
                  {'usuariosAtivos': usuariosAtivos,
                   'usuariosCadastrados':usuariosCadastrados,
                   'denunciasAceitas': denunciasAceitas,
                   'denunciasRejeitadas': denunciasRejeitadas,
                   'denunciasEA': denunciasEA,
                   'perguntas': perguntas,
                   'temas': temas
                   })

@login_required
def painel_denuncias(request, template_name="administracao/paineis/denuncias.html"):
    if request.user.is_staff == True:
        page = request.GET.get('page')
        if request.method == "POST":
            id = request.POST['id']
            status = request.POST['status']
            if id:
                denuncia = Denuncia.objects.get(pk=id)
                denuncia.verificada = status
                denuncia.save()
                return redirect('painel_denuncias')


        paginator1 = Paginator(Denuncia.objects.filter(verificada="Em Análise"), ITEMS_PER_PAGE)
        paginator2 = Paginator(Denuncia.objects.filter(verificada="Rejeitada"), ITEMS_PER_PAGE)
        paginator3 = Paginator(Denuncia.objects.filter(verificada="Aceita"), ITEMS_PER_PAGE)
        total = paginator1.count
        try:
            denunciasAceitas = paginator3.page(page)
            denunciasRejeitadas = paginator2.page(page)
            denunciasNovas = paginator1.page(page)
        except InvalidPage:
            denunciasAceitas = paginator3.page(1)
            denunciasNovas = paginator1.page(1)
            denunciasRejeitadas = paginator2.page(1)
        return render(request, template_name,
                      {'denunciasNovas': denunciasNovas,
                       'denunciasRejeitadas': denunciasRejeitadas,
                       'denunciasAceitas': denunciasAceitas
                       })
    else:
        messages.error(request, "Você não tem permissão para acessar essa página!")
        return redirect('sair_painel')

@login_required
def painel_administrativo(request, template_name="administracao/home.html"):
    if request.user.is_staff == True:
        page = request.GET.get('page')
        paginator1 = Paginator(User.objects.all(), ITEMS_PER_PAGE)
        total = paginator1.count
        try:
            usuarios = paginator1.page(page)
        except InvalidPage:
            usuarios = paginator1.page(1)
        return render(request, template_name, {'lista': usuarios})
    else:
        messages.error(request, "Você não tem permissão para acessar essa página!")
        return redirect('sair_painel')

def autenticacao_painel(request, template_name="administracao/login.html"):
    next = request.GET.get('next', '/painel')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login realizado com sucesso!")
            return HttpResponseRedirect(next)
        else:
            messages.error(request, "Apelido e/ou Senha incorretos.")
            return HttpResponseRedirect(settings.LOGIN_URL)

    return render(request, template_name, {'redirect_to':next})

def sair_painel(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)

def index(request, template_name="index.html"):
    return render(request, template_name)

def quemsomos(request, template_name="quemsomos.html"):
    return render(request, template_name)
############ ROTAS DOS CRUDS ################

#Rotas Tema
@login_required
def home_tema(request, template_name="administracao/temas/home.html"):
    if request.user.is_staff == True:
        page = request.GET.get('page')
        paginator = Paginator(Tema.objects.all(), ITEMS_PER_PAGE)
        total = paginator.count
        try:
            temas = paginator.page(page)
        except InvalidPage:
            temas = paginator.page(1)

        return render(request, template_name, {'lista':temas})
    else:
        messages.error(request, "Você não tem permissão para acessar essa página!")
        return redirect('painel_administrativo')

@login_required
def cadastrar_tema(request, template_name="administracao/temas/cadastrar.html"):
    if request.user.is_staff == True:
        try:
            form = TemaForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, "Tema cadastrado com sucesso!")
                return redirect('home_tema')
        except Exception:
            messages.error(request, "Erro ao cadastrar nova disciplina")
        return render(request, template_name, {'form': form})
    else:
        messages.error(request, "Você não tem permissão para acessar essa página!")
        return redirect('painel_administrativo')

@login_required
def info_tema(request, pk, template_name="administracao/temas/info.html"):
    if request.user.is_staff == True:
        tema = get_object_or_404(Tema, pk=pk)

        page = request.GET.get('page')
        paginator = Paginator(Nivel.objects.filter(tema=tema), ITEMS_PER_PAGE)
        total = paginator.count
        try:
            niveis = paginator.page(page)
        except InvalidPage:
            niveis = paginator.page(1)
        nivel = Nivel.objects.filter(tema=tema)
        total = nivel.count()
        try:
            form = NivelForm(request.POST or None, initial={'tema':tema})
            if form.is_valid():
                form.save()
                messages.success(request, "Nível cadastrado com sucesso!")
                return redirect('info_tema', pk=tema.pk)
        except Exception:
            messages.error(request, "Erro ao cadastrar novo nível")

        return render(request, template_name, {'tema': tema, 'lista':niveis, 'form':form, 'total':total})
    else:
        messages.error(request, "Você não tem permissão para acessar essa página!")
        return redirect('painel_administrativo')

@login_required
def editar_tema(request, pk, template_name="administracao/temas/cadastrar.html"):
    if request.user.is_staff == True:
        try:
            tema = get_object_or_404(Tema, pk=pk)
            if request.method == 'POST':
                form = TemaForm(request.POST, request.FILES, instance=tema)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Tema atualizado com sucesso!")
                    return redirect('home_tema')
            else:
                form = TemaForm(instance=tema)
        except Exception:
            messages.error(request, "Erro ao atualizar tema!")
        return render(request, template_name, {'form':form})
    else:
        messages.error(request, "Você não tem permissão para acessar essa página!")
        return redirect('painel_administrativo')

@login_required
def remover_tema(request, pk):
    if request.user.is_staff == True:
        try:
            tema = Tema.objects.get(pk=pk)
            tema.delete()
            messages.success(request, "Tema Removido com Sucesso")
        except Exception:
            messages.error(request, "Não foi possível remover tema")
        return redirect('home_tema')
    else:
        messages.error(request, "Você não tem permissão para acessar essa página!")
        return redirect('painel_administrativo')

#Rotas Níveis
@login_required
def info_nivel(request, pk, template_name="administracao/niveis/info.html"):
    if request.user.is_staff == True:
        nivel = get_object_or_404(Nivel, pk=pk)
        page = request.GET.get('page')
        paginator = Paginator(Quiz.objects.filter(nivel=nivel), ITEMS_PER_PAGE)
        total = paginator.count
        try:
            quizes = paginator.page(page)
        except InvalidPage:
            quizes = paginator.page(1)
        quiz = Quiz.objects.filter(nivel=nivel)
        total = quiz.count()
        try:
            form = QuizForm(request.POST or None, initial={'nivel':nivel})
            if form.is_valid():
                form.save()
                messages.success(request, "Pergunta cadastrada com sucesso!")
                return redirect('info_nivel', pk=nivel.pk)
        except Exception:
            messages.error(request, "Erro ao cadastrar pergunta!")
        return render(request, template_name, {'nivel': nivel, 'lista':quizes, 'total': total, 'form':form})
    else:
        messages.error(request, "Você não tem permissão para acessar essa página!")
        return redirect('painel_administrativo')

@login_required
def editar_nivel(request, pk, template_name="administracao/niveis/cadastrar.html"):
    if request.user.is_staff == True:
        try:
            nivel = get_object_or_404(Nivel, pk=pk)
            if request.method == 'POST':
                form = NivelForm(request.POST, instance=nivel)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Nível atualizado com sucesso!")
                    return redirect('info_tema', pk=nivel.tema.pk)
            else:
                form = NivelForm(instance=nivel)
        except Exception:
            messages.error(request, "Erro ao atualizar nivel!")
        return render(request, template_name, {'form':form, 'pk':nivel.tema.pk})
    else:
        messages.error(request, "Você não tem permissão para acessar essa página!")
        return redirect('painel_administrativo')

@login_required
def remover_nivel(request, pk):
    if request.user.is_staff == True:
        try:
            nivel = Nivel.objects.get(pk=pk)
            pk2 = nivel.tema.pk
            nivel.delete()
            messages.success(request, "Nível removido com Sucesso")
        except Exception:
            messages.error(request, "Não foi possível remover nível")
        return redirect('info_tema', pk=pk2)
    else:
        messages.error(request, "Você não tem permissão para acessar essa página!")
        return redirect('painel_administrativo')

#Rotas quiz
@login_required
def editar_quiz(request, pk, template_name="administracao/quiz/cadastrar.html"):
    if request.user.is_staff == True:
        try:
            quiz = get_object_or_404(Quiz, pk=pk)
            if request.method == 'POST':
                form = QuizForm(request.POST, instance=quiz)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Pergunta atualizada com sucesso!")
                    return redirect('info_nivel', pk=quiz.nivel.pk)
            else:
                form = QuizForm(instance=quiz)
        except Exception:
            messages.error(request, "Erro ao atualizar pergunta!")
        return render(request, template_name, {'form':form, 'pk':quiz.nivel.pk})
    else:
        messages.error(request, "Você não tem permissão para acessar essa página!")
        return redirect('painel_administrativo')

@login_required
def remover_quiz(request, pk):
    if request.user.is_staff == True:
        try:
            quiz = Quiz.objects.get(pk=pk)
            pk2 = quiz.nivel.pk
            quiz.delete()
            messages.success(request, "Pergunta removida com Sucesso")
        except Exception:
            messages.error(request, "Não foi possível remover pergunta")
        return redirect('info_nivel', pk=pk2)
    else:
        messages.error(request, "Você não tem permissão para acessar essa página!")
        return redirect('painel_administrativo')



#Rotas usuários
@login_required
def home_usuarios(request, template_name="administracao/usuarios/home.html"):
    if request.user.is_staff == True:
        page = request.GET.get('page')
        paginator = Paginator(User.objects.filter(is_staff=False), ITEMS_PER_PAGE)
        total = paginator.count
        try:
            usuarios = paginator.page(page)
        except InvalidPage:
            usuarios = paginator.page(1)
        return render(request, template_name, {'lista':usuarios})
    else:
        messages.error(request, "Você não tem permissão para acessar essa página!")
        return redirect('painel_administrativo')

@login_required
def info_usuarios(request, pk, template_name="administracao/usuarios/info.html"):
    if request.user.is_staff == True:
        usuario = get_object_or_404(User, pk=pk)
        return render(request, template_name, {'usuario':usuario})
    else:
        messages.error(request, "Você não tem permissão para acessar essa página!")
        return redirect('painel_administrativo')

@login_required
def remover_usuarios(request, pk):
    if request.user.is_staff == True:
        try:
            usuario = User.objects.get(pk=pk)
            user = User.objects.get(pk=usuario.user.pk)
            usuario.delete()
            user.delete()
            messages.success(request, "Usuário removido com Sucesso")
        except Exception:
            messages.error(request, "Não foi possível remover Usuário")
        return redirect('home_usuarios')
    else:
        messages.error(request, "Você não tem permissão para acessar essa página!")
        return redirect('painel_administrativo')


@login_required
def cadastro_usuario_admin(request, template_name="administracao/usuarios_administracao/cadastrar.html"):
    if request.user.is_superuser == True:
        try:
            form = UserAdminForm(request.POST or None)
            if request.method == "POST":
                if form.is_valid():
                    user = form.save(commit=False)
                    user.set_password(user.password)
                    user.is_staff = True
                    user.save()
                    messages.success(request, "Administrador criado com sucesso")
                    return redirect('home_usuario_admin')
        except Exception:
            messages.error(request, "Erro ao cadastrar usuário!")
        return render(request, template_name, {'form': form})
    else:
        messages.error(request, "Você não tem permissão para fazer isso!")
        return redirect('home_usuario_admin')

@login_required
def editar_usuario_admin(request, pk, template_name="administracao/usuarios_administracao/cadastrar.html"):
    if request.user.is_superuser == True:
        try:
            user = get_object_or_404(User, pk=pk)
            if request.method == 'POST':
                form = UserAdminForm(request.POST, instance=user)
                if form.is_valid():
                    user2 = form.save(commit=False)
                    user2.set_password(user2.password)
                    user2.is_staff = True
                    user2.save()
                    messages.success(request, "Administrador atualizado com sucesso.")
                    return redirect('home_usuario_admin')
            else:
                form = UserAdminForm(instance=user)
        except Exception:
            messages.error(request, "Erro ao atualizar usuario.")
        return render(request, template_name, {'form':form, 'user':user})
    else:
        messages.error(request, "Você não tem permissão para fazer isso!")
        return redirect('home_usuario_admin')

@login_required
def remover_usuario_admin(request, pk):
    if request.user.is_superuser == True:
        try:
            user = User.objects.get(pk=pk)
            if request.user.is_superuser:
                user.delete()
                messages.success(request, "Usuário removido com sucesso.")
            else:
                messages.error(request, "Permissão negada!")
        except Exception:
            messages.error(request, "Erro ao remover usuário.")
        return redirect('home_usuario_admin')
    else:
        messages.error(request, "Você não tem permissão para fazer isso!")
        return redirect('home_usuario_admin')

@login_required
def home_usuario_admin(request, template_name="administracao/usuarios_administracao/home.html"):
    if request.user.is_staff == True:
        user = User.objects.filter(is_staff=True)
        users = {'lista':user}
        return render(request, template_name, users)
    else:
        messages.error(request, "Você não tem permissão para acessar essa página!")
        return redirect('painel_administrativo')



