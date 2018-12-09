from django.urls import path
from .views import *

urlpatterns = [
    path('painel', painel_geral, name='painel_geral'),
    path('denuncias', painel_denuncias, name='painel_denuncias'),
    path('estatisticas', painel_estatistica, name='painel_estatistica'),
    path('home', painel_administrativo, name='painel_administrativo'),
    path('login', autenticacao_painel, name='autenticacao_painel'),
    path('logout', sair_painel, name="sair_painel"),
    path('', index, name="index"),

    #Rotas do tema
    path('temas/', home_tema, name="home_tema"),
    path('temas/cadastrar', cadastrar_tema, name="cadastrar_tema"),
    path('temas/editar/<int:pk>', editar_tema, name="editar_tema"),
    path('temas/informacoes/<int:pk>', info_tema, name="info_tema"),
    path('temas/remover/<int:pk>', remover_tema, name="remover_tema"),

    #Rotas do Nível
    path('niveis/editar/<int:pk>', editar_nivel, name="editar_nivel"),
    path('niveis/informacoes/<int:pk>', info_nivel, name="info_nivel"),
    path('niveis/remover/<int:pk>', remover_nivel, name="remover_nivel"),

    #Rotas do Quiz
    path('perguntas/editar/<int:pk>', editar_quiz, name="editar_quiz"),
    path('perguntas/remover/<int:pk>', remover_quiz, name="remover_quiz"),


    #Rotas Usuários
    path('usuarios/', home_usuarios, name="home_usuarios"),
    path('usuarios/informacoes/<int:pk>', info_usuarios, name="info_usuarios"),
    path('usuarios/remover/<int:pk>', remover_usuarios, name="remover_usuarios"),

    # Rotas Usuários da Administração
    path('usuarios_administracao/cadastro', cadastro_usuario_admin, name='cadastrar_usuario_admin'),
    path('usuarios_administracao/editar/<int:pk>', editar_usuario_admin, name='editar_usuario_admin'),
    path('usuarios_administracao/remover/<int:pk>', remover_usuario_admin, name='remover_usuario_admin'),
    path('usuarios_administracao', home_usuario_admin, name='home_usuario_admin'),
]